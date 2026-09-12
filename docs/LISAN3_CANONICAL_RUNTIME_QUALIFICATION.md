# LISAN3 — Canonical Runtime Qualification Report

**Track:** Canonical Runtime Qualification (infrastructure/governance remediation).
**Branch:** `canonical-runtime-qualification` (from `main` `6dea680052cf3ccf00ccb89396503763c0dc1839`).
**Governing principle:** *make the governed path true*, not *make the current data pass the governed path*.
**Scope boundary:** NOT canonicalization, NOT semantic requalification of the five roots, Batch 08 remains `NOT_AUTHORIZED`.
**Maximum status this track may reach:** `CANONICAL_RUNTIME_READY_FOR_FRESH_INDEPENDENT_REVIEW`.

No Batch 07 history was retroactively fabricated. No ResearchRun, IsolationState,
observation, SemanticClaim, VerificationRecord, or ACCEPTED transition was created
to pretend the file-based Batch 07 campaign ran through the DB-native runtime.
Every governed record added to the authoritative DB was genuinely produced by
repository-native services reading authority-bound on-disk artifacts.

---

## 1. Runtime DB authority decision

**`lisanapp.db` (repository root) is the authoritative governed runtime store.**
Evidence:

- It is the wired default: [`backend/infrastructure/database.py:12`](../backend/infrastructure/database.py#L12) `DEFAULT_DATABASE_PATH = REPOSITORY_ROOT / "lisanapp.db"`; same URL in `alembic.ini`.
- It is the only Alembic-governed DB: `alembic_version` = the canonical head; `database_schema_status == CURRENT`.
- `data/campaign/runtime.db` has **no `alembic_version` table** — it was built ad‑hoc via `Base.metadata.create_all` by `tools/campaign.py` (`LISAN_DATABASE_URL` override) → `database_schema_status == BLOCKED_SCHEMA`. It is a non‑governed side store and was **not** promoted.

The pre-existing blocker was a **two-DB split, not missing source data**: `lisanapp.db` held the methodology but zero corpus; `runtime.db` held the corpus/tokens but zero methodology and was unstamped.

**Hazard recorded (not changed this track):** a stale duplicate Alembic chain exists under `backend/alembic/` (head `5542b3a62e23`) that diverges from the canonical top-level `alembic/` chain (head now `f2b7d1e9a3c5`). All new migrations were placed on the **top-level** chain. Retiring the stale chain is left for a separate, reviewed change.

---

## 2. DB convergence result

Convergence is reproducible and repository-native (no raw row copy, no status flip):
`tools/converge_runtime.py` re-derives the corpus **into** `lisanapp.db` using only the governed services reading the authority-bound artifacts, then fails closed unless every result is genuine. Idempotent.

Final authoritative-DB state (see `docs/evidence/runtime/convergence_activation_evidence.json`):

| Item | Value |
|---|---|
| schema | `CURRENT` @ `f2b7d1e9a3c5` |
| corpus snapshot | `snap_tanzil_1_1_ac0724796cbb` |
| verse-level CorpusOccurrence | 6,236 |
| word-level StructuralToken | 49,968 (1,642 roots) |
| methodology revisions | `…@01784170cac4` CURRENT/eligible |

---

## 3. Tanzil production activation result — **PASS**

Executed via the real `TanzilProductionActivationService.activate` (never a hand-edited status). Independently reproduced in the authoritative DB:

- canonical artifact hash `ac0724796cbb…` (bytes 1,334,737) ✓
- identity index hash `0d0a2273e82e…` ✓
- 6,236 verses ✓; source/version Tanzil Uthmani 1.1 ✓
- `fixture_only = false` ✓; `validation_status = VALIDATED`, `activation_status = PRODUCTION_ACTIVE` ✓
- `is_production_validated(snapshot) == True`; `production_validation_failures == []` ✓
- audit row `aud_tanzil_production_activation_ac0724796cbb` actor `OWNER_AUTHORITY` ✓

Existing fail-closed negative controls (`tests/test_tanzil_production_activation.py`) remain green (wrong hash, fixture, incomplete import, wrong source/version, missing artifact, stale occurrences, competing active snapshot, ineligible methodology).

> Documentation note: `docs/canonical/ADMISSION_TANZIL.md` narrates a 2026‑08‑26 activation that the live DBs had not reflected. This track established a genuine activation in the authoritative DB; the admission record's historical provenance text was **not** rewritten (see handoff §reconciliation).

---

## 4. Methodology binding result — **PASS**

`LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4` is already co-located in the authoritative DB: `lifecycle=CURRENT`, `research_run_eligible=true`, `allowed_use=QURAN_INTERNAL_CUMULATIVE_RUN`, `source_reference=skills/lisan-semantic-extraction/SKILL.md`, and the persisted `source_sha256` **exactly equals** the live file SHA-256 (`01784170cac4…`). `methodology_authority_failures(...) == []`.

---

## 5. Occurrence model result (Track D) — word-level authority adopted

Finding: **another canonical occurrence model already existed and is now used** (Track D option 3). `CorpusOccurrence` is the Tanzil **verse-identity** record (6,236 rows, `UniqueConstraint(snapshot_id, verse_ref)`, `expression=''`) and cannot represent word occurrences such as `20:18:3:1`. The word-level authority is `StructuralToken` (word_ref, root, CONFIRMED attribution), materialized from admitted QAC morphology, with exact-set coverage in `research_coverage.py`.

The governed pipeline now treats the **confirmed StructuralToken word_refs** as the root-occurrence universe; `CorpusOccurrence` is untouched (not overloaded). `StructuralToken` rows are derived from authoritative structural data only — never from Batch 07 semantic judgments.

---

## 6. Five-root exact-set derivation — **PASS (exact agreement)**

Derived independently from admitted QAC `StructuralToken` (`tools/derive_five_root_exact_sets.py`; full word_refs in `docs/evidence/runtime/five_root_exact_set_derivation.json`), then compared **afterwards** to the frozen Batch 07 counts (never tuned):

| Root (BW) | Derived confirmed | Batch 07 | Match |
|---|---|---|---|
| ESw (ع ص و) | 12 | 12 | ✓ |
| dnw (د ن و) | 133 | 133 | ✓ |
| flH (ف ل ح) | 40 | 40 | ✓ |
| fwh (ف و ه) | 13 | 13 | ✓ |
| glm (غ ل م) | 13 | 13 | ✓ |

This is **structural occurrence counting, not semantic research**. No semantic conclusions, SemanticClaims, or VerificationRecords were created for these roots.

---

## 7. Isolation-control result (Track E) — fail-closed

Previously `IsolationState.is_contaminated` defaulted to `CLEAN` and the preflight endpoint hard-coded `CLEAN` — a run was treated as isolated with zero enforcement. Remediation:

- New `establishment_status` axis (default `NOT_ESTABLISHED`) + attestation columns (`prohibited_sources`, `input_manifest`, `attesting_actor`, `attested_at`, `audit_ref`) via additive migration `f2b7d1e9a3c5` (top-level chain).
- `BlindLabIsolationService.establish_semantic_isolation` verifies a production-valid snapshot, a CURRENT source-bound methodology and an allowed-source boundary, records the input manifest + an immutable `AuditLog`, and only then transitions `NOT_ESTABLISHED → ESTABLISHED` with `is_contaminated=CLEAN`. A contaminated run cannot be (re)established CLEAN.
- Preflight routes through establishment (409 on rejection).
- `CanonicalizationPolicy` additionally requires `establishment_status == ESTABLISHED` (the existing `is_contaminated != "CLEAN"` guard line is preserved verbatim).

A fresh run is `NOT_ESTABLISHED` and cannot be canonicalized until a genuine attestation is recorded. Honest about enforcement limits: establishment attests the governed inputs were the permitted ones; actual prohibited-source exposure remains a separate, blocking contamination event.

---

## 8. Evidence-reference result (Track F) — word_ref ↔ StructuralToken bridge

`resolve_evidence_refs` gained a deterministic `token:<word_ref>` kind (and word-level observations) resolving only within the run's corpus snapshot to the run target root's **CONFIRMED** latest-extraction StructuralToken set. Campaign artifact file paths are never evidence IDs. Negative controls (in `tests/test_canonical_runtime_qualification.py`): wrong snapshot, nonexistent word_ref, wrong root, non‑CONFIRMED, verse‑ref substitution, duplicate‑cannot‑substitute, external‑prefix smuggling.

---

## 9. Host-derived completeness result (Track G)

`derive_completeness` derives the ROOT_CONCEPT eligible universe from confirmed word_refs; a UNIVERSAL root claim requires **every** confirmed occurrence supported. Coverage is never self-certified and the campaign `research_completeness="COMPLETE"` string is never imported into a claim (no such path exists, and none was added).

---

## 10. Governance negative controls (Track I) — PASS

`tests/test_canonical_runtime_qualification.py` asserts `CanonicalizationPolicy` rejects each precondition independently: non-production snapshot, missing methodology, absent / **unestablished** / contaminated isolation, missing / non-INDEPENDENT / stale VerificationRecord, ambiguous corpus dependency, confirmed counterexample (root unity), unresolved/ smuggled evidence, synthetic-fixture guard, and **unauthorized actor** (new server-owned guard: AI/automation cannot self-accept). Existing controls unchanged.

---

## 11. Infrastructure completion gate — non-semantic smoke test — PASS

`test_nonsemantic_pipeline_smoke_reaches_accepted` drives the full mechanics end-to-end on a **synthetic root `ZZQ`** in an ephemeral DB: production snapshot → current methodology → run → genuine isolation establishment → governed word-level evidence → host-derived completeness → INDEPENDENT verification → judgment validation → canonicalization. The synthetic-fixture guard (`test_control_fixture_contract_cannot_become_canonical`) proves policy refuses real acceptance of a fixture. **No production root is used; lisanapp.db is never touched by the test.**

---

## 12. V2 runtime qualification verification

| Gate | Result |
|---|---|
| Authoritative runtime DB identified | ✓ lisanapp.db |
| Tanzil production activation | ✓ PASS |
| Methodology authority | ✓ `[]` |
| Occurrence materialization | ✓ 49,968 tokens / 1,642 roots |
| Five-root exact-set derivation reproducible | ✓ exact agreement |
| Isolation fail-closed behavior | ✓ NOT_ESTABLISHED default + establishment gate |
| Evidence-resolution | ✓ bridge + negatives |
| Host completeness | ✓ word-level, host-derived |
| Governance negative controls | ✓ all |
| No semantic research run executed for the five roots | ✓ |
| No SemanticClaim created for the five roots | ✓ (0) |
| No VerificationRecord created for the five roots | ✓ (0) |
| No ACCEPTED root | ✓ (0 production; synthetic smoke only, ephemeral) |
| Batch 07 root JSONs byte-identical | ✓ (5/5) |
| Batch 08 | `NOT_AUTHORIZED` |

**Test suite:** 251 passed (non-e2e); was 227 at baseline + 24 new qualification tests; 0 existing controls weakened.

---

## 13. Final runtime qualification status

`CANONICAL_RUNTIME_READY_FOR_FRESH_INDEPENDENT_REVIEW`

The implementation agent does **not** self-authorize semantic requalification. A fresh, read-only Sol xhigh review must return `CANONICAL_RUNTIME_INDEPENDENTLY_CONFIRMED` before any five-root semantic requalification begins. See `docs/LISAN3_CANONICAL_RUNTIME_FRESH_REVIEW_HANDOFF.md`.
