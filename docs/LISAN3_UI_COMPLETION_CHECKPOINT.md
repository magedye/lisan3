# LISAN3 UI Completion Checkpoint

Status date: 2026-08-26.

This report records implementation-side, candidate-bound evidence. It does not
create product authority or grant independent review, V4, technical release
readiness, or release acceptance.

## Scope and Candidate

- Initial task HEAD: `9cb924fd7cac8c2106258881e3b2e7253cfd4268`.
- Exact implementation candidate:
  `4a6ef34be5fd0916b9285deba96a27507bafac30`.
- The candidate is six coherent commits after the initial task HEAD:
  `2c4fac1`, `b65af12`, `fa1f651`, `dd23630`, `fd563e8`, and `4a6ef34`.
- The owner-supplied stabilization verdict remains
  `STABILIZATION_REMEDIATION_INDEPENDENTLY_CONFIRMED` for
  `f202a1e703b8da97bb0df419c9149052758505cc`; this track did not repeat or
  extend that review.
- No model, production vector population, EvidenceResolver, hybrid retrieval,
  R3, V4, release, push, or external embedding-repository work was performed.

## Completion Result

- All 28 matched Stitch pairs are classified exactly once in
  `docs/STITCH_PRODUCTION_COVERAGE_MATRIX.md`.
- Counts: 8 `CURRENT_EXECUTABLE`, 7 inventory-time `CURRENT_BACKEND_GAP`,
  0 `BLOCKED_BY_MODEL_ARTIFACT`, 1 `BLOCKED_BY_R2_CONFIRMATION`, and
  12 `REFERENCE_ONLY_OR_SUPERSEDED`.
- Every current executable surface is implemented over real current contracts.
  All seven small read gaps were resolved over already-persisted governed data.
- `semantic_differentiation_lab` remains absent and blocked by an accepted
  production model, production vectors, independently confirmed R2,
  EvidenceResolver, and R3. No placeholder route or simulated result exists.

## Production Work

- Routes completed: `/`, `/audit`, `/governance`, `/steward`, `/run/[id]`,
  `/run/[id]/blind`, `/run/[id]/knowledge`, and `/claims/[id]`.
- Reusable UI: native RTL application shell, responsive sidebar/off-canvas
  navigation, page/context primitives, confirmation dialog, four-axis status
  presentation, API fetch boundary, resource loading hook, logical-property
  responsive CSS, and explicit loading/empty/error/blocked/stale states.
- Minimal read exposure: `GET /attention`, `GET /runs/{run_id}/workspace`,
  `GET /claims/{claim_id}`, and `GET /governance/overview`.
- Workspace and run-linked claim reads fail closed unless isolation is `CLEAN`
  and the current Internal Lock condition is satisfied. A forbidden pre-lock
  Knowledge read remains a visible HTTP 403, distinct from contamination.
- The quality GET path is read-only. Historical claims may expose their
  persisted nullable run linkage without fabricating a run.
- Both committed OpenAPI documents and the generated TypeScript contract were
  regenerated and match the candidate source exactly.

## Real-Data and Authority Audit

- Production pages fetch backend state; no Stitch records, fake counts, fake
  claims, mock audit decisions, model output, vector similarity, or hardcoded
  production command payloads are present.
- Ask and run creation require explicit user inputs. Empty and unavailable
  backend states remain truthful.
- Playwright and visual verification use isolated, migrated temporary databases
  with explicit test/visual-fixture labels. Those records are test evidence,
  not production corpus or semantic authority.
- Epistemic, Review, Freshness, and Publication remain four independent axes.
  Methodological stage, purity, graph connectivity, and AI runtime state are not
  presented as semantic truth.

## Exact-Candidate Verification

The following profile ran from a clean detached checkout of
`4a6ef34be5fd0916b9285deba96a27507bafac30`:

| Check | Candidate-bound result |
|---|---|
| Full non-E2E pytest | 130 passed; 1,460 deprecation warnings; 27.90 s |
| Full Playwright | 8 passed; 43 warnings; 24.57 s |
| Ruff, all tracked Python | Passed |
| Pyright | 0 errors; 160 warnings |
| ESLint | Passed |
| Next production build | Passed; all 8 application routes emitted |
| OpenAPI and generated TypeScript regeneration | Passed; zero diff |
| `pip check` | Passed; no broken requirements |
| `npm audit --omit=dev` | Passed; 0 vulnerabilities |
| Fresh Alembic database | `80330541af56 -> f4c0a1b2c3d4 -> b7e4c1d9a5f2 -> c9e2a7f4b6d1` |
| Live route smoke | All 8 frontend document routes returned HTTP 200 |
| Browser console review | No unexpected errors on current routes; pre-lock Knowledge produced the expected fail-closed 403 |
| Lighthouse desktop Home | Accessibility 100, Best Practices 100, SEO 100, Agentic 100; 31 passed / 0 failed |
| Lighthouse mobile Claim | Accessibility 100, Best Practices 100, SEO 100, Agentic 100; 29 passed / 0 failed |
| `git diff --check` and detached tracked status | Passed / clean |

The detached checkout lacked its own `.venv`, so candidate verification used
the repository interpreter explicitly. An initial `npm ci` wrapper timed out
after the dependency graph had installed; `npm ls`, ESLint, build, Playwright,
and audit then verified the installation. One audit attempt encountered a
transient network reset; the required retry passed with zero vulnerabilities.

## Browser and Golden Evidence

Screenshots were captured from the exact candidate against an isolated fresh
database. Each captured document returned HTTP 200, had native `dir="rtl"`, and
produced no console errors:

| Evidence | Viewport | SHA-256 |
|---|---:|---|
| `docs/evidence/ui/home-desktop-4a6ef34.png` | 1440 x 1000 | `5ED00F13216668D453B5A114A8677C8F9DBEBA8A2AB98D376684BCE18D7EBD8A` |
| `docs/evidence/ui/run-tablet-4a6ef34.png` | 1024 x 1305 | `18450B4A98920026BAA1C7AC60831B7190DCDF415041E002793964EDBAE9E22B` |
| `docs/evidence/ui/claim-mobile-4a6ef34.png` | 390 x 3746 | `10F6683F73C9D4FBF763C1941C54F5C27B11FB41C67CA436B34AAE8371574097` |

Visual review compared the Golden hierarchy, navigation, density, typography,
spacing, status treatment, form affordances, and current real-data states. A
tablet content-clipping defect and an accessible-name mismatch found during
review were corrected before this candidate. Desktop, tablet, and mobile final
captures materially preserve the Golden system while deferring to canonical
real contracts where a static mock differs.

## Claim Ceiling and Remaining Boundary

Allowed claim: `IMPLEMENTED`, `TESTED`, and `VERIFIED_FOR_PROFILE` for the UI
Completion profile on the exact implementation candidate.

Not established: `INDEPENDENTLY_REVIEWED`, `TECHNICALLY_RELEASE_READY`,
`V4_COMPLETE`, or `RELEASE_ACCEPTED`. The only current Golden surface not
implemented is `semantic_differentiation_lab`, correctly blocked outside this
task. The next action is a fresh independent, read-only Sol review of the final
candidate and this evidence; it must not remediate, begin model/R2/R3/V4 work,
or self-expand scope.
