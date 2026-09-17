# Tests and Evaluations Reuse

## Evidence boundary

Repository tests prove what the code was intended to guard; this review did not rerun them and does not claim current pass status. Durable reports record candidate-bound historical executions. No existing test validates a true Quranic root-concept conclusion end to end. [TR-099]

## Existing tests to adapt directly

| Pattern/source | Classification | New-project use |
|---|---|---|
| `test_slice_b.test_observation_rejection` | `ADAPT` | Observation contract rejects semantic conclusion fields; strengthen allowed free-text controls. |
| `test_slice_b.test_contamination_audit` | `REUSE_AS_IS` | Denied source access remains distinct from actual disclosure/contamination. |
| `test_slice_c` circular rejection case | `REUSE_AS_IS` | Reject vacuous/circular falsification conditions. |
| `test_ai_runtime` Blind Lab context | `ADAPT` | Assert internal mode excludes previous/external semantic artifacts across every tool/index. |
| `test_slice_c_ai` proposal separation | `ADAPT` | Replace proposal-only rule with controlled AI decision command plus immutable record/readback. |
| `test_purity` missing evidence | `REUSE_AS_IS` | Missing/unexecuted checks remain `NOT_EVALUATED`, not clean. |
| `test_properties` AI cannot mutate official state | `REFERENCE_ONLY` | Reframe: AI cannot fabricate source/tool/verification state, though it may create semantic decisions. |
| corpus authority/parser/import tests | `ADAPT` | Exact source/hash/format/identity, malformed input, fixture quarantine, idempotency and alignment. |
| methodology source-binding tests | `ADAPT` | Bind result to exact Skill/protocol bytes; retire without rewriting history. |
| R1 graph tests | `REFERENCE_ONLY` | Dependency reachability, scope isolation, rebuildability, no canonical mutation, candidate edge labels. |
| R2 vector contract/lifecycle tests | `ADAPT` | Space/source/model/config isolation, stale exclusion, derived-state deletion, candidates cannot mutate decisions. |
| status/publication/Steward tests | `DO_NOT_REUSE` | Lisan3 governance-specific; retain only generic caller-authority lesson. |

## Legacy regression cases worth converting to semantic evals

- `QAC_GLOSS_FIREWALL_REGRESSION`: structure visible, gloss use in internal induction fails.
- `SUPPORTING_SEMANTICS_ROOT_CORE_FIREWALL_REGRESSION`: letter/form material cannot independently define root core.
- `SPARSE_EVIDENCE_CEILING_REGRESSION`: sparse evidence lowers claim scope/strength but does not fabricate certainty.
- `CRITICAL_HERITAGE_SEQUENCE_REGRESSION`: external heritage opens only after internal snapshot and cannot retroactively become internal evidence.
- `R114_MEMORY_ACCESS_GATE_REGRESSION`: prior reference before snapshot is detected.
- `R115_SIX_LAYER_OUTPUT_REGRESSION`: use as inspiration for required layer visibility, not mandatory ceremony.
- `SEMANTIC_DEPENDENCY_PROPAGATION_REGRESSION`: changed upstream result identifies affected descendants.
- `V7_CUMULATIVE_WORKFLOW_REGRESSION`: observation/hypothesis snapshot precedes controlled prior opening.

These are historical specifications whose manifest still records candidate adoption and compatibility evidence `TBD`; port scenarios, not authority labels. [TR-100]

## Required new semantic eval families

### Root/form/context conflation

- Same root, different form: form-specific feature must not enter root contribution.
- Same form, different construction: construction effect must be isolated.
- Same lexical unit, different participants/context: local effect must not become invariant.
- Ambiguous attribution: system preserves multiple layer assignments.

### Unsupported semantic claims

- Citation exists but does not support the asserted proposition.
- Evidence refs point only to interpretations or the claim itself.
- Resolved source role permits structure but not semantics.
- Fluent preferred meaning lacks counterevidence or scope.

### Omitted difficult occurrences

- Holdout contains a rare form or counterexample.
- Sample excludes the only negative cluster.
- Indexed count is complete but deep analysis omits hard cases.
- Ambiguous tokens are silently dropped.

### Hidden external-source contamination

- Direct dictionary/tafsir read before internal snapshot.
- Paraphrased external definition without citation.
- Forbidden source exposed through vector cache or graph projection.
- Blocked read versus disclosed read.
- Incomplete access log must not yield clean.

### Circular reasoning

- Claim supports its own evidence relation.
- Two hypotheses mutually confirm each other.
- Derived summary/card is used as primary evidence.
- Revised conclusion cites a prior revision without terminal Quran evidence.

### Alternatives and falsification

- Plausible H2 omitted.
- H2 is merely paraphrased H1.
- Rejection condition is vacuous or not executed.
- Injected counterexample is reinterpreted away without scope change.

### Invented distinctions

- Different forms with matched distributions; correct result is no distinction established.
- Vector neighbor has high similarity but no defensible shared semantic axis.
- System chooses a difference because the prompt presupposes one.

### Fabricated tool use

- Model reports occurrence count without query receipt.
- Tool is registered/configured but never invoked.
- Tool fails; output still says passed.
- Retry succeeds but prior failed decision artifact remains incorrectly authoritative.

### Inflated confidence

- High model self-confidence with weak evidence.
- Complete corpus count but no neighbor/falsification analysis.
- Independent reviewers share model/context but are labeled independent.
- Polished explanation raises strength without new evidence.

## Evaluation record

Each case should declare target failure, input artifacts, permitted sources, expected behavior, prohibited behavior, oracle, strength/completeness implications, independence notes and exact protocol/model/tool revisions. The legacy `test-record.schema.json` is a useful reference. [TR-101]

## Test pyramid for the first prototype

1. Deterministic unit tests: source/hash, parser/alignment, resolver, coverage, schema and receipt integrity.
2. Contract tests: every Skill output and AI decision object.
3. Semantic behavior evals: synthetic and expert-curated scenarios for conflation, contamination, alternatives, falsification and confidence.
4. End-to-end research trials: one or two real roots with exact evidence and held-out challenges.
5. Independent review: declared context/model/human class.

Do not begin with Lisan3’s full mutation, OpenAPI, browser and release stack. Add those only after a real custom engine/API/UI creates the corresponding risk. [TR-102]

## Prototype acceptance ideas

- 100% of cited Quran witnesses resolve to exact snapshot locators.
- 100% of claimed Tool executions have receipts.
- No external/parametric item is labeled primary Quran evidence.
- Injected layer-confound and circularity cases are rejected or explicitly unresolved.
- Every preferred conclusion includes a serious-alternative decision, counterevidence, executed falsification status, completeness and independence state.
- Held-out difficult cases can lower/narrow/reject a result without data loss.
- Same input/config replay preserves factual artifacts; AI variance is recorded rather than hidden.

Numeric semantic-quality thresholds require an owner-approved benchmark; none are inherited from Lisan3. [TR-103]
