import hashlib


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
