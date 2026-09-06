"""Deterministic Root Universe derivation and coverage/holdout support.

Owner Request 01 §14: a reproducible Root Universe inventory with prioritization
dimensions, deterministic occurrence-coverage validation, and holdout support —
all computed in pure code over persisted ``StructuralToken`` rows. No LLM, no
randomness: the same snapshot always yields the same universe and the same
holdout split.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models


@dataclass(frozen=True)
class RootUniverseEntry:
    root: str
    confirmed_occurrences: int
    eligible_occurrences: int
    distinct_forms: int
    distinct_verses: int
    surah_spread: int
    has_disputed: bool
    has_unresolved: bool
    is_singleton: bool
    # Prioritization dimensions (higher = more informative for calibration).
    priority_dimensions: dict[str, int]

    def as_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "confirmed_occurrences": self.confirmed_occurrences,
            "eligible_occurrences": self.eligible_occurrences,
            "distinct_forms": self.distinct_forms,
            "distinct_verses": self.distinct_verses,
            "surah_spread": self.surah_spread,
            "has_disputed": self.has_disputed,
            "has_unresolved": self.has_unresolved,
            "is_singleton": self.is_singleton,
            "priority_dimensions": dict(self.priority_dimensions),
        }


@dataclass(frozen=True)
class CoverageResult:
    root: str
    eligible_refs: tuple[str, ...]
    evidenced_refs: tuple[str, ...]
    missing_refs: tuple[str, ...]
    complete: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "eligible_count": len(self.eligible_refs),
            "evidenced_count": len(self.evidenced_refs),
            "missing_refs": list(self.missing_refs),
            "complete": self.complete,
        }


class RootUniverseService:
    @staticmethod
    def _rows(db: Session, snapshot_id: str):
        return (
            db.query(models.StructuralToken)
            .filter(models.StructuralToken.snapshot_id == snapshot_id)
            .order_by(models.StructuralToken.root, models.StructuralToken.word_ref)
            .all()
        )

    @classmethod
    def derive(cls, db: Session, snapshot_id: str) -> list[RootUniverseEntry]:
        by_root: dict[str, list] = {}
        for row in cls._rows(db, snapshot_id):
            by_root.setdefault(row.root, []).append(row)

        entries: list[RootUniverseEntry] = []
        for root in sorted(by_root):
            rows = by_root[root]
            confirmed = [
                r
                for r in rows
                if r.attribution_status
                == models.StructuralAttributionStatus.CONFIRMED.value
            ]
            forms = {r.form for r in confirmed if r.form}
            verses = {r.verse_ref for r in confirmed}
            surahs = {r.verse_ref.split(":", 1)[0] for r in confirmed}
            has_disputed = any(
                r.attribution_status
                == models.StructuralAttributionStatus.DISPUTED.value
                for r in rows
            )
            has_unresolved = any(
                r.attribution_status
                == models.StructuralAttributionStatus.UNRESOLVED.value
                for r in rows
            )
            entries.append(
                RootUniverseEntry(
                    root=root,
                    confirmed_occurrences=len(confirmed),
                    eligible_occurrences=len(rows),
                    distinct_forms=len(forms),
                    distinct_verses=len(verses),
                    surah_spread=len(surahs),
                    has_disputed=has_disputed,
                    has_unresolved=has_unresolved,
                    is_singleton=len(confirmed) == 1,
                    priority_dimensions={
                        "occurrence_count": len(confirmed),
                        "form_diversity": len(forms),
                        "surah_spread": len(surahs),
                        "structural_uncertainty": int(has_disputed) + int(has_unresolved),
                    },
                )
            )
        return entries

    @classmethod
    def occurrence_coverage(
        cls,
        db: Session,
        snapshot_id: str,
        root: str,
        evidenced_refs: set[str] | frozenset[str],
    ) -> CoverageResult:
        eligible = sorted(
            row.word_ref
            for row in cls._rows(db, snapshot_id)
            if row.root == root
            and row.attribution_status
            == models.StructuralAttributionStatus.CONFIRMED.value
        )
        eligible_set = set(eligible)
        evidenced = eligible_set & set(evidenced_refs)
        missing = tuple(sorted(eligible_set - evidenced))
        return CoverageResult(
            root=root,
            eligible_refs=tuple(eligible),
            evidenced_refs=tuple(sorted(evidenced)),
            missing_refs=missing,
            complete=bool(eligible_set) and not missing,
        )

    @staticmethod
    def holdout_split(
        refs: list[str], *, holdout_every: int = 4
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Deterministic train/holdout split by sorted position (no randomness).

        Every ``holdout_every``-th occurrence (by sorted ref) is withheld, so the
        split is reproducible across runs and machines. A root with 2 or more
        occurrences always yields at least one held-out occurrence (else the
        holdout check would silently be a no-op for the many small roots); a root
        with fewer than 2 occurrences yields an empty holdout — callers should
        treat that as "holdout not available", see ``holdout_available``.
        """
        ordered = sorted(refs)
        holdout = [r for i, r in enumerate(ordered) if (i + 1) % holdout_every == 0]
        if not holdout and len(ordered) >= 2:
            holdout = [ordered[-1]]  # guarantee a signal for small roots
        held = set(holdout)
        train = tuple(r for r in ordered if r not in held)
        return train, tuple(holdout)

    @staticmethod
    def holdout_available(refs: list[str]) -> bool:
        """A meaningful holdout needs at least two occurrences."""
        return len(set(refs)) >= 2
