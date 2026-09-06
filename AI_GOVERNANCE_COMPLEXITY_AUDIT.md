# LISAN3 AI Governance Complexity Audit

Authority: latest owner instruction, 2026-09-06  
Baseline: `5667528297f4f0f3e4b245fa47cec60e992f1798`  
Scope: semantic-research and AI-authority governance only.

## Finding

The existing design protects real risks, but it applies canonical-publication
cost to ordinary research. The concrete blocking chain is:

`7 unsupported Purity dimensions -> PURITY_CHECK FAIL -> INTERNAL_LOCK FAIL -> no SemanticClaim`

This does not prove semantic safety. It prevents a research judgment because
future extractors are absent. The current API also asks callers to repeat
corpus, methodology, authority, isolation, gate-result, reviewer and publisher
metadata that the host either already knows or must not trust.

## Mandatory classification matrix

Cost uses `L/M/H`; evidence names the current implementation fact that informed
the decision.

| ID / rule | Purpose | Failure prevented | Current enforcement | Runtime / cognitive cost | Actual value | Observed evidence of need or excess | Decision |
|---|---|---|---|---|---|---|---|
| AUTH-01 source precedence | Resolve authority conflicts | AI or a derived file redefining project authority | Prompt, AGENTS, Authority Map, skill | L / M | High | Several overlapping documents repeat the same hierarchy | `KEEP_HARD` in one canonical map; references elsewhere |
| AUTH-02 AI is proposal only | Prevent AI from making project truth | Unreviewed output becomes canonical | Prompt, canonical reference, skill, API | H / H | Boundary high; formulation excessive | API cannot persist a research judgment even when evidence is valid | `MERGE` into Research Judgment vs Canonical Acceptance |
| SRC-01 admitted Quran source | Preserve text and verse identity | Fabricated/wrong Quranic text | Corpus admission and run policy | L / L | Critical | Production snapshot checks are deterministic and operative | `KEEP_HARD` |
| SRC-02 internal source isolation | Prevent external framing during Quran-internal induction | Dictionary/tafsir/prior answer contaminates induction | Isolation state, context builder, prompt | M / M | Critical | Context isolation is stronger than textual obedience | `KEEP_HARD`; enforce by context/tool permissions |
| SRC-03 eight Purity dimensions | Diagnose methodological risks | Bias, leakage, forced unity, circularity | Purity evaluator and gate | H / H | Mixed | Seven dimensions always return `NOT_EVALUATED` because extractors do not exist | `DEMOTE_TO_DIAGNOSTIC`; actual prohibited-source exposure remains hard under SRC-02 |
| PRE-01 caller corpus snapshot | Bind run to source | Run uses an unapproved corpus | Required request field plus server validation | M / M | Input has no value | Host can enumerate production-valid snapshots | `DERIVE_AUTOMATICALLY` |
| PRE-02 caller methodology revision | Bind run to method | Run uses stale/unbound method | Required request field plus source-hash validation | M / M | Binding high; manual input low | Host knows current eligible source-bound revision | `DERIVE_AUTOMATICALLY` |
| PRE-03 caller authority context | Record authority | Caller grants itself authority | Required JSON stored verbatim | M / H | Negative | Caller-supplied authority is not authoritative | `REMOVE`; host records a minimal derived context |
| PRE-04 caller isolation payload | Configure source boundary | Wrong source policy | Client repeats target/corpus/method/source list | M / M | Negative | All fields already exist on the admitted run or canonical policy | `DERIVE_AUTOMATICALLY` |
| PRE-05 all policies before every claim | Avoid missing a possibly relevant policy | Unchecked special technique | Prompt/skill preflight checklist | H / H | Low for irrelevant techniques | Missing letter-semantics policy can block a claim that never uses it | `APPLY_ONLY_AT_CANONICALIZATION` when material; otherwise diagnostic |
| WORK-01 seven ordered research stages | Make work resumable | Lost progress | Run enum, endpoint mutations, skill script | M / H | Resume useful; ordering weak | Transitions largely mirror UI actions and do not prove method | `MERGE` into optional checkpoints; no stage is an authority gate |
| STATUS-01 epistemic axis | Represent research conclusion | Ambiguous conclusion | Claim column and UI | M / M | High | A research result needs preferred/unresolved/rejected | `MERGE` into `research_state` |
| STATUS-02 review axis | Track multi-user review workflow | Unreviewed item published | Claim column, review table, UI queues | M / H | Only valuable at canonicalization | Current product is trusted local single-user | `APPLY_ONLY_AT_CANONICALIZATION` as `verification_state` plus evidence record |
| STATUS-03 freshness axis | React to new evidence/rule revision | Stale accepted result stays accepted | Claim column and invalidation mutation | M / M | High for accepted knowledge only | Ordinary hypotheses do not need freshness administration | `MERGE` into `canonical_state=REOPEN_REQUIRED` |
| STATUS-04 publication axis | Model institutional publication | Private work is published | Claim column and publish endpoint | M / H | No current semantic-research value | No separate institutional publication workflow is in current scope | `DEFER` |
| LOCK-01 `PURITY_CHECK` gate | Require all purity checks clean | Methodological contamination | Gate evaluator/report | H / H | Low as gate | It necessarily fails while seven extractors are unsupported | `REMOVE` as gate; retain diagnostics |
| LOCK-02 `INTERNAL_LOCK` gate | Release a claim after purity/corpus/isolation | Premature canonical result | Gate evaluator/report and visibility policy | H / H | Boundary useful; mechanism redundant | It blocks research visibility and duplicates source/admission checks | `REMOVE`; direct judgment validator plus canonicalization policy replace it |
| LOCK-03 `LOCK_BLOCKED` status | Explain inability to lock | Missing prerequisites | Run and claim state | M / M | Low | It conflates insufficient evidence, missing capability, and contamination | `REMOVE`; use precise error/result state |
| GATE-01 caller GateReport payload | Record a gate decision | Forged pass | Client sends status/evidence while server ignores them | M / H | None | Redundant and misleading input surface | `REMOVE` |
| COVER-01 coverage | Prevent unsupported generalization | Partial evidence claimed as universal | Free-text coverage fields and prose | M / M | Critical | Free text is not proof and all-depth analysis is unnecessarily rigid | `KEEP_HARD`; host derives claim-sensitive coverage |
| EVID-01 evidence links | Make conclusions inspectable/reproducible | Invented or cross-run support | JSON fields with limited resolution | M / M | Critical | Existing refs can be stored without being resolved | `KEEP_HARD`; resolve every asserted evidence ref server-side |
| FALS-01 falsification | Challenge important conclusions | Attractive but unfalsifiable meaning is preferred | Structured hypotheses; optional claim string | M / M | Critical for important conclusions | Intermediate observations do not need a full falsification cycle | `KEEP_HARD` for preferred important judgments and canonicalization; `KEEP_SOFT` elsewhere |
| LAYER-01 root/form/construction/context separation | Prevent semantic attribution errors | Context or morphology loaded onto the root | Skill/prompt only | M / M | Critical | This is semantic judgment and cannot be replaced by a numeric validator | `KEEP_HARD` as output contract; code validates presence/shape, not truth |
| TRACE-01 AI/tool execution trace | Prevent fictional execution and support reproduction | Claimed tool did not run | AIExecutionRecord and dispatcher | L / L | High | Current dispatcher advertises a dummy corpus search | `KEEP_HARD`; remove simulated tool and record only actual calls |
| PROV-01 broad provenance inventory | Reproduce results | Result loses origin | Many optional metadata fields | M / H | Mixed | Some fields are never consulted by a decision | `MERGE` into run, source/method bindings, evidence refs, AI trace, and audit |
| HUMAN-01 reviewer identity from request | Track approval actor | Unauthorized approval | Caller-supplied string | M / H | Negative | Caller-supplied identity cannot establish authority | `REMOVE`; server-owned trusted-local actor |
| HUMAN-02 human review for every claim | Prevent automatic truth | AI self-acceptance | Review axis and publish policy | H / H | Excessive | Hypotheses and internal judgments are not canonical knowledge | `APPLY_ONLY_AT_CANONICALIZATION` |
| CANON-01 canonical authorization | Prevent AI self-promotion | Research judgment becomes project truth | Review + publication + two gates | H / H | Critical | The boundary is real but implemented by unrelated lifecycle axes | `KEEP_HARD` as one explicit server-owned canonicalization decision |
| MEM-01 accepted-root memory | Reuse established project knowledge | Repeated research and inconsistency | Prior-result read blocked until Internal Lock | H / M | High | `/ask` cannot retrieve a result without the obsolete lock chain | `KEEP_SOFT` for research context, `KEEP_HARD` acceptance criteria; automatic retrieval |
| INVALID-01 transitive invalidation | Reopen affected knowledge | Accepted result stays current after material change | Freshness mutation | M / M | High only for accepted results | New evidence is not currently a reopen trigger | `MERGE` into explicit `REOPEN_REQUIRED` with audit |
| REG-01 dynamic status/gate registries | Avoid frontend hard-coding | UI drifts from domain | Prompt requirement, partial code | H / H | Low at current scale | Two small authoritative enums are easier to validate end-to-end | `DEFER`; OpenAPI is the current typed contract |
| STEW-01 Steward workflow | Govern command execution | Steward self-authorizes truth | Separate command pipeline | M / M | High outside ordinary research | It need not participate in observations/hypotheses/judgments | `APPLY_ONLY_AT_CANONICALIZATION` or governance mutation |
| HIST-01 duplicate `main skills/` | Preserve migration evidence | Useful legacy text lost | Two historical long documents | H / H | Historical only | Authority Map already marks them superseded | `DEFER` as read-only reference; one active runtime skill only |
| UX-01 four-axis displays/queues | Explain state | User misreads state | Status component and pages | M / H | Low after model simplification | UI mirrors backend complexity rather than a current decision | `MERGE` into Research and Canonical state display |

## Hard-boundary evidence map

| Hard boundary | Why soft guidance is insufficient | Enforcer | Required negative proof |
|---|---|---|---|
| Admitted Quran source | A prompt cannot validate bytes or lifecycle | corpus authority + run admission | invalid/inactive snapshot rejected |
| Internal source isolation | A model can disobey prose | context builder + tool allowlist + contamination state | external semantic read blocked and logged |
| Evidence existence and lineage | A model can invent IDs | research-judgment validator | missing/cross-run refs rejected |
| Claim-sensitive coverage | A model cannot self-certify database coverage | coverage validator | incomplete universal claim rejected |
| Important-result falsification | Fluency does not establish attempted disproof | structured judgment validator | preferred important result without falsification rejected |
| Canonical authorization | AI cannot grant project authority | canonicalization policy + server-owned actor | AI/research endpoint cannot set `ACCEPTED` |
| Tool execution truth | Prompt claims are not execution evidence | dispatcher + AIExecutionRecord | unavailable/simulated tool cannot appear as executed |

## Replacement evidence for removed or softened elements

| Previous rule | Why excessive | Replacement | Risk still protected by | Verification target |
|---|---|---|---|---|
| All eight Purity dimensions block | Most cannot currently be evaluated | diagnostics with hard-blocker separation | source isolation, evidence, coverage, falsification | diagnostics never grant or block research; contamination still blocks |
| Internal Lock before any claim | Conflates research judgment and canonical truth | validated Research Judgment | canonicalization endpoint remains inaccessible to AI | AI can prefer; cannot accept |
| Four claim axes | Three model future institutional workflow | two decision-bearing states plus strength/verification attributes | explicit reopen and canonicalization policy | transition matrix tests |
| Manual authority preflight | Repeats and trusts known data | deterministic host resolution | source/method authority validators | two-field run creation and invalid-authority rejection |
| Caller gate/reviewer/publisher metadata | Untrusted and redundant | server-owned evaluation and actor | audit + policy | spoofed fields rejected by schemas |

## Complexity baseline for one ordinary root research journey

| Measure | Before | Target after |
|---|---:|---:|
| Mandatory ordered stage transitions | 7 | 0 (checkpoints remain descriptive) |
| Claim status fields routinely maintained | 4 | 1 research decision; canonical state is host-owned |
| Research gates | 2 | 0 |
| Manual run/preflight fields | 9 (5 run + 4 isolation list/fields) | 2 (target contract + expression) |
| Owner decisions before research judgment | 1 review/lock path in practice | 0 |
| Minimum semantic artifacts for an unresolved outcome | observation + hypothesis + 2 gate reports + claim | research judgment only; evidence required only when asserted |
| Generic blocking conditions | 8 Purity dimensions + corpus + isolation + lock | source/capability/evidence rules material to the claim |
| Advertised tools | 1 simulated | 0 unless a real adapter is registered |

This audit authorizes no corpus admission, retrieval redesign, publication
system, or semantic conclusion.
