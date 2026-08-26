# LISAN3 UI Governance and Data-Integrity Remediation Checkpoint

Status date: 2026-08-26.

This is implementation-side, candidate-bound evidence. It does not grant
independent review, V4, technical release readiness, or release acceptance.

## Candidate and Scope

- Starting/documentation checkpoint:
  `e0238aea767a8314463c4734a3d48c3a191e4850`.
- Failed reviewed UI candidate:
  `4a6ef34be5fd0916b9285deba96a27507bafac30`.
- Independent verdict on that candidate:
  `UI_COMPLETION_INDEPENDENT_REVIEW_FAILED`.
- Exact remediation implementation candidate:
  `43c27e6dd2393d24be21805b4b2ea42b78d15955`.
- Allowed candidate state: `IMPLEMENTED`, `TESTED`,
  `VERIFIED_FOR_PROFILE`, `AWAITING_INDEPENDENT_UI_REVIEW`.

The work is limited to the five blocking governance/data-integrity findings.
No UI redesign, model integration, production vector activation, R2, R3, V4,
release action, push, or `LISAN-Quran-Embedding` change occurred. R1 independent
confirmation remains unchanged.

## Blocker Results

### Claim release and Ask

Root cause: direct claim access failed closed, but multiple derived reads used
independent or absent checks. Ask selected a matching claim without applying
the release boundary.

Result: `ClaimReleasePolicy` is the shared primitive for direct claim,
provenance, reproduction manifest, quality, history, legacy Explorer, Ask,
workspace and aggregate claim projections, audit filtering, and R1 graph
projection/read. Release requires an existing linked run, `CLEAN` isolation,
and a dynamically valid current Internal Lock. Before release, Ask reports
`INSUFFICIENT_EVIDENCE`; after release, it returns the governed claim.

### Run admission

Root cause: `POST /runs` persisted arbitrary free-text Corpus and Methodology
identifiers, and the frontend presented those strings as governed resources.

Result: run admission now validates current Corpus authority and Methodology
authority. Unknown snapshots return 422. Current known snapshots and arbitrary
Methodology revisions fail closed with 503 because no authority-bound,
production-active Corpus or canonical Methodology registry/fallback exists.
The Run Builder exposes the blockers and renders no free-text authority fields.

### Steward results

Root cause: a placeholder path returned fixed evaluated rules, `PASS`,
`SUCCESS`, and a successful audit event without dispatching a domain action.

Result: no command is claimed executable. Arbitrary commands produce an honest
`UNSUPPORTED` persisted/audited result with no evaluated rules. Commands that
attempt to cross immutable authority boundaries produce `REJECTED`, HTTP 403,
and only the actual rejection audit.

### Four independent status axes and historical data

Root cause: unofficial values (`PENDING_REVIEW`, `UNPUBLISHED`, `BLOCKED`) were
used by defaults/transitions/fixtures, review rejection mutated Publication,
and frontend substring tones could make noncanonical/private values look
positive.

Result: models, schemas, transitions, fixtures, and presentation use the exact
canonical Epistemic, Review, Freshness, and Publication vocabularies. Database
CHECK constraints reject unofficial values. Review rejection changes only the
Review axis. Unknown UI values are neutral and marked `CONTRACT_DEFECT`.

Migration `d4f7a2c8e901` reconciles only known legacy/null states, records
before/after state in `RECONCILE_CANONICAL_STATUS_AXES` audit events, refuses
unknown meaning, and has a tested downgrade. The local current database had no
claims requiring reconciliation.

### Quality read model

Root cause: a missing persisted QualityProfile manufactured fixed coverage and
reproducibility values.

Result: persisted profiles are returned unchanged. With no profile, the API
identifies only deterministic methodological purity as derived; corpus/deep
coverage, reproducibility, conflict burden, and leak metrics remain null. The
frontend renders QualityProfile as unavailable/not evaluated.

## Candidate-Bound Verification

The final profile ran from a clean detached checkout of
`43c27e6dd2393d24be21805b4b2ea42b78d15955`. A first detached run of the prior
candidate `a0963689b135509dcfd09fd4763de1c2bd15059d` exposed three Slice G tests
that depended on an ambient ignored database; the defect was classified
`TEST_DEFECT`, the tests were isolated, and a new candidate was created before
verification restarted.

| Check | Exact-candidate result |
|---|---|
| Focused adversarial profile | 9 production-path tests passed within the full suite |
| Full pytest | 156 passed |
| Explicit Playwright journeys | 8 passed; 47 deprecation warnings |
| Ruff, all tracked Python | Passed |
| Pyright | 0 errors; 177 existing SQLAlchemy-style warnings |
| ESLint | Passed |
| Next production build | Passed; all current application routes emitted |
| OpenAPI and TypeScript regeneration | Passed; zero diff; both OpenAPI SHA-256 `D36EEBE320CDFC144E95A44268C511C9DC48B5006548897F753396D309A02922` |
| Alembic | Fresh base-to-head reached `d4f7a2c8e901`; model parity and four axis constraints passed |
| `pip check` | No broken requirements |
| `npm audit --omit=dev` | 0 vulnerabilities |
| Route smoke | Health 200; readiness 200; Ask 200 insufficient; unknown run 422 |
| `git diff --check`, tracked diff/status | Passed; clean |

The focused adversarial suite proves unreleased semantic/evidence/audit markers
cannot escape any inventoried claim-derived read API; release enables the same
resources; unknown/unadmitted runs cannot persist; arbitrary Steward commands
cannot claim success; noncanonical axes cannot persist or cross-mutate; and a
missing QualityProfile cannot create invented metrics.

## Remaining Boundary and Next Action

No blocking defect remains inside this remediation scope. Current Corpus and
Methodology authority remains unavailable by canonical design, so Run Builder
correctly stays unavailable. The Governance ARIA tab pattern remains a
non-blocking separate UI-quality follow-up because its component was not
touched.

Exact next action: perform one fresh, independent, read-only UI Completion
review of implementation candidate
`43c27e6dd2393d24be21805b4b2ea42b78d15955` and the direct documentation-only
checkpoint containing this report. Reproduce the five original counterexamples
and bind the verdict to both exact SHAs; do not remediate or begin model,
production vector, R2/R3, V4, or release work in that review context.
