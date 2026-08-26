import hashlib
import json
from dataclasses import dataclass
from typing import Any

from backend.domain.services.corpus.authority import CorpusAdmissionRecord

TANZIL_SOURCE_ID = "TANZIL_QURAN_UTHMANI"
TANZIL_VERSION = "1.1"
TANZIL_RIGHTS_MARKER = "Tanzil Quran Text (Uthmani, Version 1.1)"
STANDARD_VERSE_COUNTS = (
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99,
    128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38,
    29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18,
    12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29,
    19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8,
    11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6,
)


@dataclass(frozen=True)
class TanzilVerse:
    surah: int
    ayah: int
    line_number: int
    verse_ref: str
    text: str


@dataclass(frozen=True)
class TanzilArtifactResult:
    actual_sha256: str
    artifact_size_bytes: int
    identity_index_sha256: str
    verses: tuple[TanzilVerse, ...]


class TanzilArtifactParser:
    """Validate the authority-bound Tanzil 1.1 bytes and verse identity index."""

    def __init__(self, admission: CorpusAdmissionRecord):
        self.admission = admission

    def parse(self, raw_bytes: bytes, index_bytes: bytes) -> TanzilArtifactResult:
        self._validate_admission_contract()
        actual_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        if actual_sha256 != self.admission.expected_hash:
            raise ValueError(
                "Tanzil artifact hash mismatch: expected "
                f"{self.admission.expected_hash}, got {actual_sha256}"
            )
        if len(raw_bytes) != self.admission.expected_bytes:
            raise ValueError(
                "Tanzil artifact byte-size mismatch: expected "
                f"{self.admission.expected_bytes}, got {len(raw_bytes)}"
            )

        index_sha256 = hashlib.sha256(index_bytes).hexdigest()
        if index_sha256 != self.admission.identity_index_sha256:
            raise ValueError("Tanzil identity index hash mismatch")
        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            raise ValueError("Tanzil artifact must not contain a UTF-8 BOM")
        if b"\r" in raw_bytes:
            raise ValueError("Tanzil artifact must use LF-only newlines")
        if not raw_bytes.endswith(b"\n"):
            raise ValueError("Tanzil artifact must end with an LF newline")
        try:
            decoded_artifact = raw_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ValueError("Tanzil artifact is not valid UTF-8") from exc
        if TANZIL_RIGHTS_MARKER not in decoded_artifact:
            raise ValueError("Tanzil 1.1 source/version rights marker is missing")

        raw_lines = raw_bytes.split(b"\n")[:-1]
        decoded_data_lines: dict[int, str] = {}
        for line_number, line_bytes in enumerate(raw_lines, start=1):
            if not line_bytes or line_bytes.startswith(b"#"):
                continue
            if line_bytes != line_bytes.strip() or b"\t" in line_bytes:
                raise ValueError(
                    f"Malformed Tanzil record at physical line {line_number}"
                )
            try:
                decoded_data_lines[line_number] = line_bytes.decode(
                    "utf-8", errors="strict"
                )
            except UnicodeDecodeError as exc:
                raise ValueError(
                    f"Malformed UTF-8 Tanzil record at physical line {line_number}"
                ) from exc

        index = self._load_identity_index(index_bytes)
        indexed_identities = self._flatten_identity_index(index)
        indexed_lines = [line for _, _, line in indexed_identities]
        if indexed_lines != list(decoded_data_lines):
            raise ValueError(
                "Tanzil records do not reconcile exactly with identity-index lines"
            )

        verses = tuple(
            TanzilVerse(
                surah=surah,
                ayah=ayah,
                line_number=line_number,
                verse_ref=f"{surah}:{ayah}",
                text=decoded_data_lines[line_number],
            )
            for surah, ayah, line_number in indexed_identities
        )
        if len(verses) != self.admission.expected_verse_count:
            raise ValueError(
                "Tanzil verse count mismatch: expected "
                f"{self.admission.expected_verse_count}, got {len(verses)}"
            )
        return TanzilArtifactResult(
            actual_sha256=actual_sha256,
            artifact_size_bytes=len(raw_bytes),
            identity_index_sha256=index_sha256,
            verses=verses,
        )

    def _validate_admission_contract(self) -> None:
        if self.admission.source_id != TANZIL_SOURCE_ID:
            raise ValueError("Wrong canonical source for Tanzil import")
        if self.admission.canonical_text_version != TANZIL_VERSION:
            raise ValueError("Wrong canonical Tanzil version")
        required = (
            self.admission.expected_hash,
            self.admission.expected_bytes,
            self.admission.identity_index_sha256,
            self.admission.expected_verse_count,
        )
        if any(value is None for value in required):
            raise ValueError("Tanzil authority is missing a bound artifact constraint")

    def _load_identity_index(self, index_bytes: bytes) -> dict[str, Any]:
        try:
            loaded = json.loads(index_bytes.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Tanzil identity index is malformed") from exc
        if not isinstance(loaded, dict):
            raise TypeError("Tanzil identity index must be an object")
        expected_metadata = {
            "artifact": "quran_verse_index",
            "version": "1.0.0",
            "source_sha256": self.admission.expected_hash,
            "verse_count": self.admission.expected_verse_count,
            "surah_count": 114,
        }
        for key, expected in expected_metadata.items():
            if loaded.get(key) != expected:
                raise ValueError(
                    f"Tanzil identity index {key} does not match authority"
                )
        return loaded

    @staticmethod
    def _flatten_identity_index(
        index: dict[str, Any],
    ) -> list[tuple[int, int, int]]:
        surahs = index.get("surahs")
        if not isinstance(surahs, list) or len(surahs) != 114:
            raise ValueError("Tanzil identity index must cover exactly 114 surahs")
        identities: list[tuple[int, int, int]] = []
        seen_refs: set[tuple[int, int]] = set()
        seen_lines: set[int] = set()
        previous_line = 0
        for expected_surah, (surah_entry, expected_count) in enumerate(
            zip(surahs, STANDARD_VERSE_COUNTS, strict=True), start=1
        ):
            if not isinstance(surah_entry, dict):
                raise TypeError("Tanzil identity index has a malformed surah")
            if surah_entry.get("surah") != expected_surah:
                raise ValueError("Tanzil surah identities are missing or out of order")
            if surah_entry.get("verse_count") != expected_count:
                raise ValueError(
                    f"Tanzil surah {expected_surah} has an impossible verse count"
                )
            verses = surah_entry.get("verses")
            if not isinstance(verses, list) or len(verses) != expected_count:
                raise ValueError(
                    f"Tanzil surah {expected_surah} has missing or extra identities"
            )
            for expected_ayah, verse_entry in enumerate(verses, start=1):
                if not isinstance(verse_entry, dict):
                    raise TypeError("Tanzil identity index has a malformed verse")
                ayah = verse_entry.get("ayah")
                line_number = verse_entry.get("line")
                if ayah != expected_ayah or type(line_number) is not int:
                    raise ValueError("Tanzil ayah identities are missing or out of order")
                verse_ref = (expected_surah, expected_ayah)
                if verse_ref in seen_refs or line_number in seen_lines:
                    raise ValueError("Tanzil identity index contains a duplicate")
                if line_number <= previous_line:
                    raise ValueError("Tanzil identity-index lines are out of order")
                seen_refs.add(verse_ref)
                seen_lines.add(line_number)
                previous_line = line_number
                identities.append((expected_surah, expected_ayah, line_number))
        if len(identities) != 6_236:
            raise ValueError("Tanzil identity index must contain exactly 6,236 verses")
        return identities


class TanzilAdapter:
    """
    Adapter for Tanzil Quranic Text (Uthmani).
    Responsible for validating hash, parsing XML/txt, and extracting exact text safely.
    """

    def __init__(self, expected_hash: str = None):
        self.expected_hash = expected_hash

    def parse_corpus(self, raw_text: str) -> list[dict]:
        """
        Parses Tanzil standard format: Surah|Ayah|Text
        """
        # Validate hash if expected_hash is provided
        actual_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        if self.expected_hash and actual_hash != self.expected_hash:
            raise ValueError(
                f"Tanzil hash mismatch. Expected {self.expected_hash}, got {actual_hash}"
            )

        occurrences = []
        for line_num, line in enumerate(raw_text.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("|")
            if len(parts) >= 3:
                surah, ayah, text = parts[0], parts[1], parts[2]
                occurrences.append(
                    {
                        "verse_ref": f"{surah}:{ayah}",
                        "text": text,
                        "surah": int(surah),
                        "ayah": int(ayah),
                    }
                )

        return occurrences
