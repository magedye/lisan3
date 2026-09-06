"""Deterministic loader for qualified structural-annotation fixtures.

Loads a QAC-style structural fixture (root/form per word occurrence) into the
persisted ``StructuralToken`` store so Root Descriptive Profiles become reusable
and reproducible. This is a pure parse+insert of an already-qualified structural
fixture; it derives no meaning and invents no attribution.

The QAC morphology corpus itself is not yet admitted (SOURCE_ROLE_PENDING,
license pending — see docs/canonical/ADMISSION_QAC.md), so the only qualified
structural data available for the full corpus is absent. This loader qualifies
the *capability* against the bundled ``slm_full_fixture.csv`` (root س ل م).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from backend.domain import models

SLM_FIXTURE_SOURCE_ID = "QAC_MORPHOLOGY_WEB_V0_4_FIXTURE"
SLM_FIXTURE_SOURCE_VERSION = "v0.4"
SLM_FIXTURE_EXTRACTION_VERSION = "slm-fixture-v1"
DEFAULT_SLM_FIXTURE = Path("data/fixtures/structural/slm_full_fixture.csv")


@dataclass(frozen=True)
class StructuralImportResult:
    snapshot_id: str
    rows_processed: int  # CSV rows upserted; re-load is idempotent (deterministic ids)
    roots: tuple[str, ...]


class StructuralFixtureLoader:
    @staticmethod
    def load_slm_fixture(
        db: Session,
        snapshot_id: str,
        *,
        csv_path: Path | None = None,
    ) -> StructuralImportResult:
        path = csv_path or DEFAULT_SLM_FIXTURE
        rows = StructuralFixtureLoader._read_rows(path)
        roots: set[str] = set()
        rows_processed = 0
        for row in rows:
            surah = row["surah"].strip()
            ayah = row["ayah"].strip()
            word_ref = row["qac_word_ref"].strip()
            root = row["root"].strip()
            roots.add(root)
            token = models.StructuralToken(
                id=f"stok_{snapshot_id}_{word_ref.replace(':', '_')}",
                snapshot_id=snapshot_id,
                word_ref=word_ref,
                verse_ref=f"{surah}:{ayah}",
                root=root,
                form=row["derived_form_group"].strip() or None,
                pos_tag=None,
                source_id=row.get("source_id", SLM_FIXTURE_SOURCE_ID).strip()
                or SLM_FIXTURE_SOURCE_ID,
                source_version=SLM_FIXTURE_SOURCE_VERSION,
                extraction_version=SLM_FIXTURE_EXTRACTION_VERSION,
                attribution_status=models.StructuralAttributionStatus.CONFIRMED.value,
            )
            db.merge(token)  # idempotent re-load (deterministic id)
            rows_processed += 1
        db.commit()
        return StructuralImportResult(
            snapshot_id=snapshot_id,
            rows_processed=rows_processed,
            roots=tuple(sorted(roots)),
        )

    @staticmethod
    def _read_rows(path: Path) -> list[dict]:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
