"""Real Quranic Arabic Corpus (QAC) morphology v0.4 importer.

Admits the QAC morphology artifact as a LOCAL, hash-bound, acquire-per-install
immutable structural source and persists its root/form attributions as governed
``StructuralToken`` rows (INT-PRE-OWN-001). The raw GPL artifact is never edited
in place and never redistributed via this repo (see docs/canonical/ADMISSION_QAC.md);
the importer fails closed if the source bytes drift from the qualified SHA-256.

Source: Quranic Arabic Corpus (morphology, v0.4), (C) 2011 Kais Dukes, GNU GPL.
Attribution required in derived works: "Quranic Arabic Corpus (Kais Dukes, 2011),
http://corpus.quran.com". QAC builds structural annotation over the Tanzil text;
Tanzil remains the sole Quran-text / verse-identity authority — QAC FORM never
overwrites Tanzil text.

Roots are kept in the source's Buckwalter encoding as the stable, unambiguous key
(a transliteration helper is provided for display only).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from backend.domain import models

QAC_SOURCE_ID = "QAC_MORPHOLOGY"
QAC_SOURCE_VERSION = "0.4"
QAC_EXTRACTION_VERSION = "qac-0.4-import-v1"
QAC_EXPECTED_SHA256 = (
    "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
)
QAC_EXPECTED_BYTES = 6309503
QAC_LICENSE = "GNU General Public License"
QAC_COPYRIGHT = "Copyright (C) 2011 Kais Dukes"
QAC_ATTRIBUTION = "Quranic Arabic Corpus (Kais Dukes, 2011), http://corpus.quran.com"
QAC_SOURCE_URL = "http://corpus.quran.com/download"
QAC_ACQUISITION_MIRROR = (
    "https://raw.githubusercontent.com/bnjasim/quranic-corpus/"
    "74416e4881d79e09713c170c7234226cb1785555/quranic-corpus-morphology-0.4.txt"
)
DEFAULT_QAC_ARTIFACT = Path("data/corpus/qac/quranic-corpus-morphology-0.4.txt")

_HEADER = "LOCATION\tFORM\tTAG\tFEATURES"
_LOC_RE = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
# Buckwalter -> Arabic letters (display only; the Buckwalter form remains the key).
_BW2AR = {
    "'": "ء", "|": "آ", ">": "أ", "&": "ؤ", "<": "إ", "}": "ئ", "A": "ا", "b": "ب",
    "p": "ة", "t": "ت", "v": "ث", "j": "ج", "H": "ح", "x": "خ", "d": "د", "*": "ذ",
    "r": "ر", "z": "ز", "s": "س", "$": "ش", "S": "ص", "D": "ض", "T": "ط", "Z": "ظ",
    "E": "ع", "g": "غ", "f": "ف", "q": "ق", "k": "ك", "l": "ل", "m": "م", "n": "ن",
    "h": "ه", "w": "و", "y": "ي", "Y": "ى", "{": "ٱ",
}


def buckwalter_to_arabic(root: str) -> str:
    return " ".join(_BW2AR.get(ch, ch) for ch in root)


@dataclass(frozen=True)
class QacSegment:
    surah: int
    ayah: int
    word: int
    segment: int
    form: str
    tag: str
    root: str | None
    pos: str | None
    verb_form: str | None

    @property
    def verse_ref(self) -> str:
        return f"{self.surah}:{self.ayah}"

    @property
    def word_ref(self) -> str:
        return f"{self.surah}:{self.ayah}:{self.word}:{self.segment}"


@dataclass(frozen=True)
class QacImportResult:
    snapshot_id: str
    source_sha256: str
    segments_total: int
    root_bearing_segments: int
    distinct_roots: int
    tokens_persisted: int
    reconciliation: dict


_VERB_FORM_RE = re.compile(r"^\((I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\)$")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_segments(raw_bytes: bytes) -> list[QacSegment]:
    """Deterministically parse the QAC morphology TSV. Fails closed on any format
    deviation from the qualified v0.4 structure."""
    text = raw_bytes.decode("ascii")  # QAC v0.4 is strict ASCII; non-ASCII => error
    lines = text.splitlines()  # tolerant of CRLF/LF; raw-byte SHA guards integrity
    try:
        header_idx = lines.index(_HEADER)
    except ValueError as exc:
        raise ValueError("QAC header 'LOCATION FORM TAG FEATURES' not found") from exc

    segments: list[QacSegment] = []
    seen: set[str] = set()
    for line in lines[header_idx + 1 :]:
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 4:
            raise ValueError(f"QAC row does not have exactly 4 TSV fields: {line!r}")
        loc, form, tag, feats = parts
        m = _LOC_RE.match(loc)
        if not m:
            raise ValueError(f"Malformed QAC location: {loc!r}")
        if loc in seen:
            raise ValueError(f"Duplicate QAC location: {loc!r}")
        seen.add(loc)
        surah, ayah, word, segment = (int(g) for g in m.groups())
        tokens = feats.split("|")
        root = None
        pos = None
        verb_form = None
        for tok in tokens:
            if tok.startswith("ROOT:"):
                root = tok[5:]
            elif tok.startswith("POS:"):
                pos = tok[4:]
            elif _VERB_FORM_RE.match(tok):
                verb_form = tok.strip("()")
        segments.append(
            QacSegment(
                surah=surah, ayah=ayah, word=word, segment=segment,
                form=form, tag=tag, root=root, pos=pos, verb_form=verb_form,
            )
        )
    return segments


class QacMorphologyImporter:
    @staticmethod
    def _form_label(seg: QacSegment) -> str:
        base = seg.pos or seg.tag or "UNK"
        return f"{base}({seg.verb_form})" if seg.verb_form else base

    @classmethod
    def import_tokens(
        cls,
        db: Session,
        snapshot_id: str,
        *,
        artifact_path: Path | None = None,
    ) -> QacImportResult:
        path = artifact_path or DEFAULT_QAC_ARTIFACT
        raw = path.read_bytes()
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != QAC_EXPECTED_SHA256 or len(raw) != QAC_EXPECTED_BYTES:
            raise ValueError(
                "QAC artifact bytes do not match the qualified immutable source "
                f"(sha256={actual_sha}, bytes={len(raw)}); refusing to import."
            )

        segments = parse_segments(raw)
        root_segments = [s for s in segments if s.root]

        # Reconcile against the Tanzil verse identity held in this snapshot.
        tanzil_verses = {
            str(v)
            for (v,) in db.query(models.CorpusOccurrence.verse_ref)
            .filter(models.CorpusOccurrence.snapshot_id == snapshot_id)
            .all()
        }
        qac_verses = {s.verse_ref for s in segments}
        unmatched = sorted(qac_verses - tanzil_verses) if tanzil_verses else []
        if tanzil_verses and unmatched:
            raise ValueError(
                f"{len(unmatched)} QAC verse references are absent from the "
                f"admitted Tanzil snapshot (e.g. {unmatched[:3]}); failing closed."
            )
        reconciliation = {
            "tanzil_verse_authority": "Tanzil owns verse identity; QAC never overwrites text.",
            "qac_verse_count": len(qac_verses),
            "tanzil_verse_count": len(tanzil_verses),
            "verse_sets_equal": bool(tanzil_verses) and qac_verses == tanzil_verses,
            "unmatched_qac_verses": unmatched,
            "known_word_offset_notes": {
                "opening_basmala_verses_offset": 112,
                "residual_word_count_exceptions": ["2:181", "8:6", "13:37", "37:130"],
                "note": "QAC word indices exclude the 112 embedded opening-basmala tokens Tanzil 1.1 includes; four residual ba'da-ma / internal-space cases documented in Stage-A. Verse identity matches exactly.",
            },
            "embedded_qac_tanzil_version": "1.0.2",
            "active_tanzil_version": "1.1",
        }

        # Idempotent reload: replace this source's tokens for the snapshot.
        db.query(models.StructuralToken).filter(
            models.StructuralToken.snapshot_id == snapshot_id,
            models.StructuralToken.extraction_version == QAC_EXTRACTION_VERSION,
        ).delete(synchronize_session=False)

        rows = [
            models.StructuralToken(
                id=f"stok_qac_{snapshot_id}_{s.surah}_{s.ayah}_{s.word}_{s.segment}",
                snapshot_id=snapshot_id,
                word_ref=s.word_ref,
                verse_ref=s.verse_ref,
                root=s.root,
                form=cls._form_label(s),
                pos_tag=s.pos or s.tag,
                source_id=QAC_SOURCE_ID,
                source_version=QAC_SOURCE_VERSION,
                extraction_version=QAC_EXTRACTION_VERSION,
                attribution_status=models.StructuralAttributionStatus.CONFIRMED.value,
            )
            for s in root_segments
        ]
        db.bulk_save_objects(rows)
        db.commit()

        return QacImportResult(
            snapshot_id=snapshot_id,
            source_sha256=actual_sha,
            segments_total=len(segments),
            root_bearing_segments=len(root_segments),
            distinct_roots=len({s.root for s in root_segments}),
            tokens_persisted=len(rows),
            reconciliation=reconciliation,
        )
