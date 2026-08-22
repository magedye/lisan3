import typing


class QACAdapter:
    """
    Adapter for Quranic Arabic Corpus (QAC).
    Responsible for parsing structural elements while strictly quarantining semantic ontology.
    """

    ALLOWED_FEATURES: typing.ClassVar[set] = {"POS", "ROOT", "LEMMA", "MORPH", "SYNTAX"}
    FORBIDDEN_FEATURES: typing.ClassVar[set] = {"SEMANTIC_TAG", "ONTOLOGY"}

    def parse_corpus(self, raw_text: str) -> list[dict]:
        """
        Parses QAC format. Expects format:
        LOCATION | FORM | TAG | FEATURES
        e.g., (1:1:1:1) | bi | P | ...
        """
        structural_tokens = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("|")
            if len(parts) >= 4:
                location, form, tag = parts[0], parts[1], parts[2]

                # Strip out semantic features
                clean_features = []
                for feature in parts[3:]:
                    # In a real QAC parser, this would be a robust regex or mapping matching exact QAC semantic tags.
                    if "SEM:" in feature.upper() or "ONTOLOGY:" in feature.upper():
                        continue  # Quarantine
                    clean_features.append(feature)

                loc_parts = location.strip("()").split(":")
                if len(loc_parts) == 4:
                    surah, ayah, word, part = loc_parts

                    structural_tokens.append(
                        {
                            "verse_ref": f"{surah}:{ayah}",
                            "word_idx": int(word),
                            "part_idx": int(part),
                            "form": form,
                            "pos_tag": tag,
                            "features": ":".join(clean_features),
                        }
                    )

        return structural_tokens
