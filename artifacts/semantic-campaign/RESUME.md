# Root-Research Campaign — Deterministic Resume

A fresh session resumes with **no conversation history** using only the committed
ledger + `CampaignState` + this file.

## Prerequisites
- Runtime DB (gitignored): rebuilt by `bootstrap`.
- QAC morphology artifact (acquire-per-install, GPL, not committed):
  `data/corpus/qac/quranic-corpus-morphology-0.4.txt`
  SHA-256 `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`.
  If absent, acquire a byte-identical copy (e.g. the pinned mirror in
  `docs/canonical/ADMISSION_QAC.md`) — the importer fail-closes on any SHA drift.

## 0. Bootstrap runtime (idempotent)
```
python tools/campaign.py bootstrap      # loads Tanzil + QAC if the DB is empty
python tools/campaign.py status         # processed vs remaining; research vs canon
```

## Pipeline per batch (each stage persists after every root)
1. **Select** a diverse batch:
   `python tools/campaign.py select --n 40`  -> space-separated Buckwalter roots
2. **Prep** full-coverage packets:
   `python tools/campaign.py prep --roots "<roots>" --out data/campaign/packets/<batch>`
3. **Discovery + adversarial verify** (workflow `root-research-full-coverage`):
   args `{dir: data/campaign/packets/<batch>, roots: [{root, file}, ...]}`
   -> reconstruct combined `[{root, judgment, verdict}]`.
4. **Exact-set coverage** — shard, map every word_ref, deep-analyze resistant cases:
   `python tools/campaign.py prep-coverage --results <combined.json> --out data/campaign/coverage/<batch>`
   then workflow `coverage-mapping` with args `{dir, roots:[{root, shards, file}]}`;
   reconstruct via a journal parser into coverage results.
5. **Persist** with validation:
   `python tools/campaign.py persist-coverage --research <combined.json> --coverage <coverage.json> --batch <batch>-coverage`
   -> per-root artifact in `artifacts/semantic-campaign/roots/`, exact-set validated,
   ledger + CampaignState updated (idempotent; lineage preserved on reprocess).

## Current state (as of Window 03 / Batch 05 closure)
- Processed **88 / 1,642** roots; remaining **1,554**; `PENDING_COVERAGE_EVIDENCE = 0`;
  all processed roots exact-set COMPLETE; canonicalization PENDING for all.
- No interrupted work. Next action: run the per-batch pipeline for Batch 06.
- Report: `docs/LISAN3_WINDOW_03_BATCH_05.md`.

## Filename safety (IMPORTANT — do not regress)
`tools/campaign.py safe_name` escapes the uppercase Buckwalter homograph letters
`H S D T Z` (e.g. `S`→`_53_`) as well as FS-illegal chars, because the QAC universe
has 137 case-fold pairs (e.g. `Swm` ص و م vs `swm` س و م) that otherwise share one
artifact file on a case-insensitive filesystem and silently overwrite each other.
Per-root artifact files are named `safe_name(root).json`; never assume the raw root
is the filename.

## Invariants (never weaken)
- `ROOT_SEMANTIC_UNITY = NON_NEGOTIABLE`: one unreconciled confirmed occurrence
  blocks `universal_presence_holds`; one missing confirmed word_ref blocks
  `research_completeness=COMPLETE`. No majority/percentage.
- Research proceeds without human canonicalization; `canonical_authorization`
  stays `PENDING` (a valid strong research result is not canonical truth).
- Coverage is word_ref-level exact-set (never verse_ref; never model-claimed counts).
