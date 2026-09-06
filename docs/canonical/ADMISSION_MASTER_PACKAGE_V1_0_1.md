# Master Integrated Package v1.0.1 — LISAN3 Admission Record

**authority revision**: `LISAN3_MASTER_PACKAGE_ADMISSION_V1_2026_09_06`
**package**: `Quran_Lisan_Master_Integrated_Package` version `1.0.1`
**package status (as declared)**: `MASTER_v1.0.1_ROOT_SEMANTIC_UNITY_FIXED`
**admission verdict**: `MASTER_ADMITTED_AND_PRE_ANALYSIS_FOUNDATION_QUALIFIED`
**admission mode**: conservative, reuse-first, hash-bound. No package bytes are
copied into the tracked tree; nothing in V2.1 is edited in place.

This is the single authority pointer for the package. It records *where the
package governs*, *what it does not govern*, and *how each accepted owner
directive is already realized* in this repository — so no artifact is duplicated
and no OPEN proposal is silently promoted.

## 1. Package identity (bound by hash, not by bytes)

- Local archive (non-tracked): `Quran_Lisan_Master_Integrated_Package_v1.0.1.zip`
- Archive SHA-256:
  `4f88c3556e32ce0c5697db6acfaf711c7d03e05179863964fe57c8cae021268b`
- Extracted (non-tracked) working copy:
  `Quran_Lisan_Master_Integrated_Package_v1.0.1/…`
- Per-file identity is carried by the package's own
  `SHA256SUMS.txt` / `PACKAGE_MANIFEST.json` (300 files). Governing files cited
  below are pinned by those hashes, e.g.
  `00_START_HERE/00_MASTER_AUTHORITY.md` =
  `41f0784b62d090da9f06b8628bef89ce746bf6073bbd30c890550d9a19b32c4c`.

The archive is retained locally as evidence/reference only. It is deliberately
kept out of source history (see repository `.gitignore`); this admission record
plus the hash above are the tamper-evident binding.

## 2. Authority precedence (per package `00_MASTER_AUTHORITY.md`)

1. Latest explicit owner instruction.
2. The **accepted** post-V2.1 owner directives in
   `02_CURRENT_OWNER_DIRECTIVES/` (the governing delta over V2.1).
3. `01_CANONICAL_BASE/Quran_Lisan_Complete_Package_V2.1.0/` as the preserved
   canonical base, except where `05_REGISTRIES/MASTER_SUPERSESSION_MAP.csv`
   records an explicit conflict resolved by a newer owner directive.
4. Governed capture policy + traceability.
5. Contracts, registries, executable tests.
6. `03_PRE_ANALYSIS/` and the proposal rows in `05_REGISTRIES/` are **OPEN /
   non-governing** until owner acceptance.
7. `06_RESEARCH_REFERENCES/` and `90_ARCHIVE/` are comparison/history only and
   hold no authority to change methodology.

This record subordinates to the repository's existing
`SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md` and the canonical
references it names; it adds the package's owner-directive delta on top, it does
not replace them.

## 3. What is governing vs. archive

| Package area | Disposition |
|---|---|
| `02_CURRENT_OWNER_DIRECTIVES/` (INT-* accepted directives) | **GOVERNING DELTA** over V2.1 |
| `00_START_HERE/` (authority, status, execution order) | GOVERNING (orientation + precedence) |
| `05_REGISTRIES/MASTER_SUPERSESSION_MAP.csv` | GOVERNING (conflict resolutions) |
| `01_CANONICAL_BASE/…V2.1.0/` | PRESERVED CANONICAL BASE (reference; never edited here) |
| `04_RUNTIME_PROMPTS/` | GOVERNING only alongside this package during semantic runs |
| `03_PRE_ANALYSIS/` | **OPEN / NON-GOVERNING** (planning proposals; P1..P8 not adopted) |
| `05_REGISTRIES/*` proposal rows (change proposals, open questions) | OPEN capture backlog (archive/reference) |
| `06_RESEARCH_REFERENCES/`, `90_ARCHIVE/` | REFERENCE / HISTORY only |

## 4. Accepted directive → realization map (reuse-first; no duplication)

| Directive | Substance | Realized in repo by |
|---|---|---|
| `INT-BOOT-001` Governed capture | capture→classify→disposition, owner≠proposal | Existing `ChangeProposal(status)` + `RuleRevision(approved_by)` + `GovernanceRule` + `AuditLog` + Steward boundary. Package `05_REGISTRIES` CSVs admitted as archive. Bound by `tests/test_phase0a_pre_analysis_foundation.py::test_8…` |
| `INT-PRE-OWN-001` Descriptive knowledge first | deterministic facts before semantic reasoning; 3 knowledge levels | New deterministic read-model `backend/domain/services/corpus/descriptive_profile.py` over existing `QACAdapter`/`CorpusOccurrence`/`CorpusSnapshot`. Architecture form (persisted store) left **OPEN** per GQ-PRE-003. Bound by `test_1/2/3…` |
| `INT-OWN-ROOT-001/002` Root semantic unity (NON_NEGOTIABLE) | unifying meaning in every confirmed occurrence; no majority substitute | Existing exact-coverage rule (`research_judgment.derive_completeness`) + new canonicalization guard in `backend/domain/services/canonicalization.py`. Bound by `test_4/5…` and existing `LISAN_PURITY_AND_STRUCTURAL_EVIDENCE_CONTRACT.md` |
| `INT-EXT-001..007` External hypothesis policy | external = hypothesis/test, no authority; Jabal = high-priority hypothesis, no bonus, never canonical; external ≠ blind-internal | Existing isolation (`BlindLabIsolationService`, `IsolationState`) + methodology immutability + new additive `Hypothesis.origin` marker. Bound by `test_6/7…` |
| `INT-OWN-TERM-001` Terminology clarity | reduce ambiguous «دلالة» / «الوحدة المعجمية» in new human-facing text; no technical rename | Human-facing delta reused verbatim from package `05_TERMINOLOGY_CLARITY_DELTA.md`; no code/ID rename performed |

## 5. Preservation guarantee (no silent rewrite)

- No file under `01_CANONICAL_BASE/…V2.1.0/` is modified. The V2.1 base is
  bound by its own manifest hashes and remains untouched.
- Admitted corpus/methodology provenance is immutable at the persistence layer
  (SQLAlchemy events on `CorpusSnapshot` / `MethodologyRevision`), verified by
  `tests/test_phase0a_pre_analysis_foundation.py::test_9…`.
- Conflicts between V2.1 and the newer owner delta are resolved only through the
  recorded rows in `MASTER_SUPERSESSION_MAP.csv` (SUP-004/005/006/009), never by
  in-place edits.

## 6. Not admitted / deferred to owner (do not adopt silently)

- P1..P8 as a formal program structure (`SUP-007`, `OPEN_NOT_CANONICAL`).
- A permanent full dual-lane Blind/External lifecycle (`SUP-008`,
  `OPEN_NOT_CANONICAL`) — the lighter `Hypothesis.origin` marker is used instead.
- A persisted `StructuralToken` / standalone Root-Profile authority store
  (GQ-PRE-003 / CP-PRE-003, `PROPOSAL_CREATED`).
- An `EXTERNAL_HYPOTHESIS_REGISTER` table and `claim_type` taxonomy (open
  non-owner implementation proposals in the external-hypothesis policy).
- Any full V2.1 terminology rename.
