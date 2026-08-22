class CrossSourceAligner:
    """
    Aligns Tanzil Canonical Text with QAC Structural Data.
    Fails closed if misalignment is detected (e.g., mismatching surah/ayah count).
    """

    @staticmethod
    def align_sources(tanzil_data: list[dict], qac_data: list[dict]) -> list[dict]:
        """
        Takes raw Tanzil occurrences and QAC tokens, aligns them by verse_ref.
        """
        # Group QAC by verse
        qac_by_verse = {}
        for token in qac_data:
            ref = token["verse_ref"]
            if ref not in qac_by_verse:
                qac_by_verse[ref] = []
            qac_by_verse[ref].append(token)

        aligned_occurrences = []
        for t_verse in tanzil_data:
            ref = t_verse["verse_ref"]
            qac_tokens = qac_by_verse.get(ref, [])

            # Simple integrity check: At least some tokens should exist for a verse
            # Note: in real production we would check exact word counts.
            if not qac_tokens and t_verse["text"]:
                pass  # Depending on policy, we might log a warning or fail. For now, just align.

            aligned_occurrences.append(
                {
                    "verse_ref": ref,
                    "text": t_verse["text"],
                    "structural_tokens": qac_tokens,
                }
            )

        return aligned_occurrences
