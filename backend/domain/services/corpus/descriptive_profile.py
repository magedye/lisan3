"""Deterministic, reproducible Root Descriptive Profile (المعرفة قبل الاجتهاد).

Owner directive INT-PRE-OWN-001 / Request 01 §6: whatever can be established by
enumeration, counting, matching and disciplined extraction is derived ONCE,
verifiably, persisted (as ``StructuralToken`` rows), and reused — never re-guessed
by an LLM inside every RootRun. A profile is a deterministic read-model / VIEW
over those governed rows; it asserts NO semantic meaning.

Four knowledge levels are kept distinct so a reviewable structural annotation is
never presented as a direct textual fact:

  - DIRECT_TEXTUAL_FACT: verse/word references and text-derived distribution.
  - QUALIFIED_STRUCTURAL_ANNOTATION: confirmed root/form attribution + its counts.
  - DISPUTED_STRUCTURAL_ANNOTATION: a contested attribution to this root.
  - UNRESOLVED_STRUCTURAL_ANNOTATION: an attribution not yet resolved.

All aggregation is ordered and computed in pure Python: the same tokens and root
always produce a byte-identical profile.
"""

from __future__ import annotations

import enum
from collections import Counter, defaultdict
from dataclasses import dataclass, field

# Structural attribution status carried by each token (mirrors
# models.StructuralAttributionStatus).
ATTR_CONFIRMED = "CONFIRMED"
ATTR_DISPUTED = "DISPUTED"
ATTR_UNRESOLVED = "UNRESOLVED"

EXTRACTION_METHOD = "DETERMINISTIC_CODE_AGGREGATION_NO_LLM"


class KnowledgeLevel(str, enum.Enum):
    DIRECT_TEXTUAL_FACT = "DIRECT_TEXTUAL_FACT"
    QUALIFIED_STRUCTURAL_ANNOTATION = "QUALIFIED_STRUCTURAL_ANNOTATION"
    DISPUTED_STRUCTURAL_ANNOTATION = "DISPUTED_STRUCTURAL_ANNOTATION"
    UNRESOLVED_STRUCTURAL_ANNOTATION = "UNRESOLVED_STRUCTURAL_ANNOTATION"


@dataclass(frozen=True)
class StructuralToken:
    """One structural-source attribution of a word occurrence to a root."""

    word_ref: str
    verse_ref: str
    root: str
    form: str | None = None
    pos_tag: str | None = None
    attribution_status: str = ATTR_CONFIRMED


@dataclass(frozen=True)
class FormProfile:
    form: str
    count: int
    occurrence_refs: tuple[str, ...]
    knowledge_level: KnowledgeLevel = KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION


@dataclass(frozen=True)
class RootDescriptiveProfile:
    """A reusable descriptive profile for a single root. Meaning-free."""

    root: str
    source_id: str | None
    source_version: str | None
    extraction_version: str | None
    verification_state: str
    structural_source_reviewable: bool
    extraction_method: str

    # Direct textual facts.
    occurrence_refs: tuple[str, ...]
    verse_refs: tuple[str, ...]
    surah_distribution: dict[str, int]

    # Qualified structural annotations.
    total_confirmed_occurrences: int
    total_eligible_occurrences: int
    forms: tuple[FormProfile, ...]
    singleton_forms: tuple[str, ...]

    # Reviewable annotations, preserved and never hidden.
    disputed_annotations: tuple[dict[str, str], ...]
    unresolved_annotations: tuple[dict[str, str], ...]

    knowledge_levels: dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "source_id": self.source_id,
            "source_version": self.source_version,
            "extraction_version": self.extraction_version,
            "verification_state": self.verification_state,
            "structural_source_reviewable": self.structural_source_reviewable,
            "extraction_method": self.extraction_method,
            "occurrence_refs": list(self.occurrence_refs),
            "verse_refs": list(self.verse_refs),
            "surah_distribution": dict(self.surah_distribution),
            "total_confirmed_occurrences": self.total_confirmed_occurrences,
            "total_eligible_occurrences": self.total_eligible_occurrences,
            "forms": [
                {
                    "form": f.form,
                    "count": f.count,
                    "occurrence_refs": list(f.occurrence_refs),
                    "knowledge_level": f.knowledge_level.value,
                }
                for f in self.forms
            ],
            "singleton_forms": list(self.singleton_forms),
            "disputed_annotations": [dict(d) for d in self.disputed_annotations],
            "unresolved_annotations": [dict(d) for d in self.unresolved_annotations],
            "knowledge_levels": dict(self.knowledge_levels),
        }


# Every field of a ROOT-scoped profile is conditioned on root attribution (a
# reviewable structural annotation), so no field is a bare DIRECT_TEXTUAL_FACT:
# the locations are listed *because* the structural source attributes them to the
# root. Labelling a derived count DIRECT while its total is QUALIFIED would be an
# internal contradiction, so all confirmed-set fields share the QUALIFIED label.
# DIRECT_TEXTUAL_FACT remains defined for expression/lexeme-scoped facts.
_ROOT_PROFILE_KNOWLEDGE_LEVELS: dict[str, str] = {
    "root": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "occurrence_refs": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "verse_refs": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "surah_distribution": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "total_confirmed_occurrences": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "total_eligible_occurrences": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "forms": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "singleton_forms": KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value,
    "disputed_annotations": KnowledgeLevel.DISPUTED_STRUCTURAL_ANNOTATION.value,
    "unresolved_annotations": KnowledgeLevel.UNRESOLVED_STRUCTURAL_ANNOTATION.value,
}


def _annotation(token: StructuralToken, reason: str) -> dict[str, str]:
    return {
        "word_ref": token.word_ref,
        "verse_ref": token.verse_ref,
        "form": token.form or "UNCLASSIFIED",
        "reason": reason,
    }


class RootDescriptiveProfileService:
    """Builds a :class:`RootDescriptiveProfile` deterministically from tokens."""

    @staticmethod
    def _surah_of(verse_ref: str) -> str:
        return verse_ref.split(":", 1)[0] if ":" in verse_ref else verse_ref

    @classmethod
    def build(
        cls,
        root: str,
        tokens: list[StructuralToken],
        *,
        source_id: str | None = None,
        source_version: str | None = None,
        extraction_version: str | None = None,
        verification_state: str = "UNVERIFIED",
        structural_source_reviewable: bool = True,
    ) -> RootDescriptiveProfile:
        eligible = [t for t in tokens if t.root == root]
        confirmed = sorted(
            (t for t in eligible if t.attribution_status == ATTR_CONFIRMED),
            key=lambda t: t.word_ref,
        )
        disputed = sorted(
            (t for t in eligible if t.attribution_status == ATTR_DISPUTED),
            key=lambda t: t.word_ref,
        )
        unresolved = sorted(
            (t for t in eligible if t.attribution_status == ATTR_UNRESOLVED),
            key=lambda t: t.word_ref,
        )

        occurrence_refs = tuple(t.word_ref for t in confirmed)
        verse_refs = tuple(dict.fromkeys(t.verse_ref for t in confirmed))

        surah_counter: Counter[str] = Counter(
            cls._surah_of(t.verse_ref) for t in confirmed
        )
        surah_distribution = {k: surah_counter[k] for k in sorted(surah_counter)}

        form_refs: dict[str, list[str]] = defaultdict(list)
        for t in confirmed:
            form_refs[t.form or "UNCLASSIFIED"].append(t.word_ref)
        forms = tuple(
            FormProfile(form=form, count=len(refs), occurrence_refs=tuple(refs))
            for form, refs in sorted(form_refs.items())
        )
        singleton_forms = tuple(f.form for f in forms if f.count == 1)

        disputed_annotations = tuple(
            _annotation(t, "structural attribution to this root is contested")
            for t in disputed
        )
        unresolved_annotations = tuple(
            _annotation(t, "structural attribution to this root is unresolved")
            for t in unresolved
        )

        return RootDescriptiveProfile(
            root=root,
            source_id=source_id,
            source_version=source_version,
            extraction_version=extraction_version,
            verification_state=verification_state,
            structural_source_reviewable=structural_source_reviewable,
            extraction_method=EXTRACTION_METHOD,
            occurrence_refs=occurrence_refs,
            verse_refs=verse_refs,
            surah_distribution=surah_distribution,
            total_confirmed_occurrences=len(confirmed),
            total_eligible_occurrences=len(eligible),
            forms=forms,
            singleton_forms=singleton_forms,
            disputed_annotations=disputed_annotations,
            unresolved_annotations=unresolved_annotations,
            knowledge_levels=dict(_ROOT_PROFILE_KNOWLEDGE_LEVELS),
        )

    @classmethod
    def build_from_snapshot(cls, db, snapshot_id: str, root: str):
        """Build a profile from persisted ``StructuralToken`` rows.

        Provenance (source, extraction version, verification state) is READ from
        the governed rows and the ``CorpusSnapshot``; nothing is re-derived by a
        model. Returns ``None`` if the root has no tokens in the snapshot.
        """
        from backend.domain import models

        all_rows = (
            db.query(models.StructuralToken)
            .filter(
                models.StructuralToken.snapshot_id == snapshot_id,
                models.StructuralToken.root == root,
            )
            .order_by(models.StructuralToken.word_ref)
            .all()
        )
        if not all_rows:
            return None
        # A snapshot may hold more than one extraction version for the same
        # word_ref (the unique key permits it). Build from exactly ONE version —
        # the latest deterministically — so occurrences are never double-counted
        # and provenance is uniform.
        chosen_version = max(r.extraction_version for r in all_rows)
        rows = [r for r in all_rows if r.extraction_version == chosen_version]
        tokens = [
            StructuralToken(
                word_ref=r.word_ref,
                verse_ref=r.verse_ref,
                root=r.root,
                form=r.form,
                pos_tag=r.pos_tag,
                attribution_status=r.attribution_status,
            )
            for r in rows
        ]
        snapshot = db.get(models.CorpusSnapshot, snapshot_id)
        first = rows[0]
        return cls.build(
            root,
            tokens,
            source_id=first.source_id,
            source_version=first.source_version,
            extraction_version=first.extraction_version,
            verification_state=(
                snapshot.validation_status if snapshot is not None else "UNVERIFIED"
            ),
            structural_source_reviewable=True,
        )

    @staticmethod
    def tokens_from_qac(
        qac_tokens: list[dict],
        *,
        disputed_word_refs: frozenset[str] | None = None,
    ) -> list[StructuralToken]:
        """Adapt :class:`QACAdapter` output into structural tokens (root read from
        the ``ROOT`` feature). No re-derivation."""
        disputed = disputed_word_refs or frozenset()
        tokens: list[StructuralToken] = []
        for tok in qac_tokens:
            features = tok.get("features", "") or ""
            feats = features.split(":")
            root = None
            for i, part in enumerate(feats[:-1]):
                if part.upper() == "ROOT":
                    root = feats[i + 1]
                    break
            if not root:
                continue
            word_ref = f"{tok['verse_ref']}:{tok.get('word_idx')}:{tok.get('part_idx')}"
            tokens.append(
                StructuralToken(
                    word_ref=word_ref,
                    verse_ref=tok["verse_ref"],
                    root=root,
                    form=tok.get("pos_tag"),
                    pos_tag=tok.get("pos_tag"),
                    attribution_status=(
                        ATTR_DISPUTED if word_ref in disputed else ATTR_CONFIRMED
                    ),
                )
            )
        return tokens
