# LISAN3 — Owner Request 02 Execution Record

**status**: `BLOCKED_PENDING_QAC_MORPHOLOGY_ADMISSION`
**verdict**: `SEMANTIC_CAMPAIGN_AT_CURRENT_QUALIFIED_LIMIT` (current qualified limit = **0 processable roots** due to an irreducible external-data blocker)
**machine-readable**: `artifacts/semantic-campaign/CAMPAIGN_STATUS.json`
**reads handoff**: `artifacts/semantic-campaign/PHASE_1_HANDOFF.json` (candidate `7594fb45`)

## What was done (Request 02 §1)
1. Read the Phase 1 handoff and verified the candidate/runtime against it.
2. Confirmed the pre-analysis foundation is fully qualified (Request 01, 179 tests).
3. **Executed a runtime derivation check**: seeded the production-active Tanzil
   snapshot (`snap_tanzil_1_1_ac0724796cbb`, 6236 verses) and called
   `RootUniverseService.derive(...)`. Result: **0 structural tokens → 0 eligible
   roots**. There is no morphological root→word attribution for the admitted
   corpus.

## Why the campaign cannot process any root (honestly, without fabrication)
- The **QAC morphology corpus** — the only source that assigns roots to Quranic
  words — is `SOURCE_ROLE_PENDING`: its license (GPLv3 / CC terms) is unreconciled
  and its artifact is external and uncommitted (`docs/canonical/ADMISSION_QAC.md`).
  Obtaining/redistributing it needs an owner license decision and bytes not
  available to the runtime.
- The only structural data present is the bundled `slm` (س ل م) **prototype**
  fixture, explicitly `semantic_evidence_allowed=false` and not proven-complete.
  Using it to produce accepted semantic root results would violate its own
  governance marker.
- Request 01 **FP-3** requires proven descriptive completeness *before*
  universal-presence testing. That precondition cannot be met without the full
  morphology corpus, so root semantic unity could not be honestly evaluated even
  for a single root.
- Fabricating morphology or root meanings would violate the non-negotiable
  evidence-integrity invariant (Request 01 §3.4). The methodology is designed to
  **fail closed** here rather than generate answers.

This is exactly the campaign's design goal: *qualified roots, not generated
answers* (Request 02 §2). With no qualified source data, the qualified count is 0.

## Stop condition
Request 02 §20.3 — *an essential source/runtime dependency is unavailable*. This
is the single irreducible blocker; all independent work that could be done without
the data was completed in Request 01.

## Counts
| metric | value |
|---|---|
| eligible roots | 0 (universe underivable without QAC morphology) |
| processed roots | 0 |
| accepted roots | 0 |
| unresolved roots | 0 |
| blocked/ineligible roots | all (pending QAC) |
| methodology revisions created | 0 |
| evaluation cases added | 0 (25+ were added in Request 01 for the machinery) |
| external hypotheses tested | 0 |
| cross-root hypotheses generated | 0 |

## What IS ready (so resumption is immediate once unblocked)
Every campaign capability is built and test-qualified (Request 01): Root Universe
derivation, Root Descriptive Profile, deterministic coverage, holdout, root
semantic unity enforcement, unified external-hypothesis register, internal/external
isolation, accepted-root memory with reopen, and campaign checkpoint/resume. The
runner needs **only the source data**.

## What would permit additional roots to become eligible
Owner reconciles the QAC morphology license and admits the artifact (hash-bound),
or provides an equivalent qualified morphology source. Then a real QAC importer
persists `structural_tokens` for the full corpus, `RootUniverseService.derive`
yields the real eligible roots, and this campaign resumes automatically and
processes roots to the qualified limit — no conversational context required
(`CAMPAIGN_STATUS.json` + `PHASE_1_HANDOFF.json` fully describe the state).

## Owner decision required to proceed
Admit a qualified Quranic morphology source (QAC license reconciliation, or an
alternative). This is the sole gate between the qualified foundation and a real
large-scale root campaign.
