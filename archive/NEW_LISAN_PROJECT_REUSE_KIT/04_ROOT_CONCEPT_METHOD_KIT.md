# Root Concept Method Kit

## Purpose and evidence boundary

This document reconciles current Lisan3 material relevant to discovering and testing a root semantic core. It is an extraction and recommendation input, not the final Root Concept Contract for the new project. Canonical/active-derived observations are distinguished from recommendations. [TR-013]

## Working object

Lisan3’s strongest methodological definition is: the Root Core is the minimum positive semantic structure defensible as stable and distinctive within a declared root scope after separating form, construction and context. The Skill separately presents Root Definition, Root Meaning and Root Concept; these are views of the result, not independent evidence. Source: `skills/lisan-semantic-extraction/SKILL.md` §§3–4, 9, 21. [TR-014]

For the new project, treat the object initially as a **root-concept hypothesis over one or more explicitly identified lexical units**, not as an assumed single essence.

## Inputs

| Input | Lisan3 basis | Reuse assessment |
|---|---|---|
| Target expression and analysis unit | Skill §§1–2; `ResearchRun.target_contract/target_expression` | Adapt: add lexical-unit identity, orthographic normalization and ambiguity set. |
| Quran snapshot | Tanzil admission; `CorpusSnapshot` | Reuse source identity/hash/version/count principles. |
| Complete indexed occurrence inventory | Skill §6/Phase 1 | Reuse requirement; current Lisan3 runtime cannot satisfy token/root inventory with verse-only occurrences. |
| Token/segment morphology and permitted syntax | Purity contract §Future structural annotation | Adapt minimal provenance-bound record; never infer silently from model memory. |
| Structural observations | Skill Phase 2; `ObservationArtifact` | Reuse fields, but type them and link each to exact locators. |
| Context windows and clusters | Skill Phases 2–3 | Adapt with declared window policy and cluster rationale. |
| Candidate lexical-unit partition | Skill §12.1 | Add as first-class input/output because current models lack it. |
| Prior hypotheses and revisions | `Hypothesis`, legacy freeze schema | Adapt with immutable revision lineage and influence log. |
| Essential neighbors and comparison axes | Skill Phases 5–6; `EssentialNeighbor` | Reuse method, not fixed neighbor counts. |
| Source-role/access profile | Blind Lab, QAC admission, Purity contract | Reuse mechanism; redesign phases for higher AI authority. |
| Tool execution evidence | Tool Reality §15; `AIExecutionRecord` | Adapt to per-invocation receipts. |

## Analysis units and scoping

The method must select one primary unit: root contribution, lexical unit, morphological form, construction, local meaning, or broader concept. A root project also needs an explicit `LEXICAL_UNIT_SET` because the same orthographic root may support multiple lexical units or unresolved branches. Source: Skill §§2, 12. [TR-015]

Recommended scope record:

```yaml
target:
  root_identity: "..."
  orthographic_policy: "..."
  lexical_unit_hypotheses: ["LU1", "LU2"]
  included_forms: ["..."]
  excluded_forms_and_reason: ["..."]
  corpus_snapshot: "..."
  claim_scope: "..."
```

## Derivational coverage

Lisan3 requires separating index coverage from deep analysis and reporting form/construction/context/neighbor coverage. For large roots, a stratified sample may support exploration but not an unqualified generalization. Source: Skill §6. [TR-016]

The new project should record:

- total target occurrences and how target identity was determined;
- coverage by lemma, derivation, inflection, form/pattern, voice and relevant features;
- rare/exceptional forms;
- forms excluded because of unresolved morphology;
- deep-analysis sample method and holdout/challenge set;
- whether each lexical-unit hypothesis has adequate coverage.

## Layer separation procedure

For every proposed invariant, test in order:

1. Does it recur across the claimed lexical/root scope?
2. Does it occur only in one form or derivation?
3. Is it supplied by transitivity, a preposition or another construction?
4. Is it a property of agent, patient, affected entity or result?
5. Is it an event consequence rather than lexical contribution?
6. Is it discourse/pragmatic/tafsir/fiqh interpretation?
7. Does it disappear while the root/lexical unit remains?

Source: Skill §11. This sequence directly attacks root/form/construction/context conflation. [TR-017]

## Participant roles

Participant structure is both a potential differentiator and a confounder. Record role inventory per occurrence before inferring semantics: initiator/agent, affected entity, endpoint, instrument, beneficiary, experiencer, source/path/goal, and implicit participants where structurally licensed. Do not import the participant’s properties into the root concept merely because they co-occur. Source: Skill Phase 2 and differentiation axes. [TR-018]

## Contextual clustering

Clusters may use form, construction, participant pattern, event type and discourse domain, but the cluster label is not the definition. [TR-019]

Recommended checks:

- cluster stability under alternative feature choices;
- whether a cluster maps to a form/construction rather than lexical split;
- outliers and difficult occurrences assigned explicitly;
- no “miscellaneous” bucket hidden from completeness;
- cluster names phrased descriptively, not semantically conclusively.

## Competing hypotheses

Retain a primary candidate, serious alternatives, and the possibility that current evidence establishes no qualified invariant. Freeze each serious hypothesis before its full challenge set so it cannot be silently rewritten after failures. Source: Skill Phase 4 and legacy `initial-hypothesis-freeze-v1`. [TR-020]

Each hypothesis should contain:

- exact statement and scope;
- lexical-unit/branch assignment;
- predicted positive and negative distributions;
- layer attribution assumptions;
- supporting evidence relations;
- strongest counterevidence;
- unresolved cases;
- rejection/narrowing/reopen condition;
- revision parent and reason for change.

## Semantic neighbors and distinctive features

Select essential neighbors because they share a domain, participant/event structure or apparent substitutability—not because they are easy to distinguish. Substitution is a probe, not proof. Apply only evidence-bearing axes such as event type, agency, intentionality, participants, direction, aspect, result, affected entity, syntax, morphology, distribution, collocation, scalarity and temporal profile. Source: Skill Phases 5–6 and §8. [TR-021]

The desired output is the smallest positive discriminating feature or feature set that:

- is compatible with target evidence;
- survives removal of form/construction/context effects;
- distinguishes essential neighbors;
- predicts at least some positive/negative cases;
- is falsifiable;
- is not invented merely because forms differ.

## Hard cases

Hard cases are mandatory challenge material, not exclusions of convenience:

- rare form or construction;
- apparently contradictory occurrence;
- ambiguous segmentation/root assignment;
- occurrence fitting more than one lexical-unit hypothesis;
- apparent metaphor or discourse-driven shift;
- closest semantic neighbor in a near-identical construction;
- negative case where the hypothesized feature should appear but does not;
- external/traditional definition that frames the evidence too neatly.

The semantic-pilot evidence shows why this matters operationally: Lisan3 could verify verse identity but not exact root/form/construction coverage, so it correctly left Root Core null rather than use orthographic guesses or model memory. Source: semantic-pilot blocker report and corrective addendum. [TR-022]

## Counterevidence, falsification and rejection

An operational rejection condition names:

- observable trigger;
- canonical search space;
- verification method;
- confound controls for form/construction/context;
- decision effect: reject, narrow, split, reopen or remain unresolved.

Circular phrases such as “reject if wrong” are structurally rejected in `schemas.RejectionCondition` and `test_slice_c.py`. The new project should go further by executing the search and attaching a receipt; schema validity alone does not prove falsification occurred. [TR-023]

## Lexical-unit ambiguity, polysemy and homonymy

Do not assume a single root concept. Compare at least these live possibilities when warranted:

- one lexical unit with context-conditioned realizations;
- multiple lexical units sharing a defensible superordinate root contribution;
- multiple branches with no established superordinate;
- unresolved segmentation or root identity;
- historical homonymy claim, which requires evidence beyond Quran-internal distribution.

Keep separate coverage/evidence/counterevidence/status per branch. Do not pool one branch’s evidence to manufacture another’s stability. Source: Skill §12.1. [TR-024]

## Unresolved outcomes

A valid result can be:

- preferred hypothesis with bounded strength;
- two or more live alternatives;
- a narrowed lexical-unit-specific result;
- root contribution not established but local meanings established;
- structurally blocked/incomplete;
- no meaningful difference established between forms or neighbors.

The new project should not inherit `LOCK_BLOCKED` as its general lifecycle, but it should preserve honest non-resolution and explicit reason codes. [TR-025]

## Confidence implications

Root-concept strength should increase with independent admissible evidence, coverage diversity, discrimination, prediction, falsification survival and reproducibility, and decrease with unresolved counterevidence, layer attribution uncertainty, source contamination risk and incomplete coverage. It must remain separate from research completeness and independent verification. Lisan3 warns against uncalibrated percentages, while its current `QualityProfile` fields are not a validated confidence model. [TR-026]

## Known failure modes

| Failure | Detection/response |
|---|---|
| Dictionary-first | Check event chronology, access logs and influence lineage; do not infer cleanliness from missing logs. |
| Contextual leakage | Compare claimed feature across controlled form/construction/participant settings. |
| Root-form conflation | Contrast forms within lexical unit and same form across contexts. |
| Structural overpromotion | Require independent semantic distribution evidence. |
| Generic overextraction | Essential-neighbor, negative and predictive tests. |
| Forced unification | Preserve branches and excluded counterexamples; test superordinate separately. |
| Neighbor cherry-picking | Record candidate-generation method and why each neighbor is essential/excluded. |
| Coverage inflation | Separate indexed/analyzed/validated denominators. |
| Circular confirmation | Traverse support graph to primary evidence; remove derived restatements. |
| Tool simulation | Require server-owned execution receipt, not model prose. |
| Invented distinction | Permit `NO_DIFFERENCE_ESTABLISHED`; require positive evidence for every axis. |
| Presentation-as-proof | Treat definition elegance as output quality only. |

## Relevant existing tests and their limits

- `test_slice_b.py`: rejects an unapproved semantic field in structural observations; proves blocked read is not contamination. Useful pattern, fixture-only.
- `test_slice_c.py`: rejects circular rejection conditions, stores neighbor analysis, and blocks a claim when computed Internal Lock fails. It does not test a valid Quranic root concept.
- `test_properties.py`: useful invariant/property patterns, but primarily governance/state authority.
- `test_purity.py`: proves missing evidence remains `NOT_EVALUATED` and detects simple hypothesis-before-observation; the evaluator is not semantically complete.
- Legacy regressions: QAC gloss firewall, supporting-semantics firewall, sparse-evidence ceiling, six-layer output, heritage sequence and hypothesis freeze are high-value scenario designs, but their manifest still says candidate/TBD and they are not current Lisan3 authority.
- R2 benchmark: demonstrates that aggregate similarity can hide task/space false positives; use as a retrieval warning, not a semantic oracle.

## A. Reuse unchanged

1. Quran-internal induction as the primary evidence path.
2. Explicit analysis unit and scope.
3. Root/form/construction/roles/context separation.
4. Counterevidence, unresolved cases and failed predictions as first-class.
5. Operational rejection conditions.
6. No forced single root concept.
7. Substitution as a probe, not independent proof.
8. Distinct indexed, deeply analyzed and validated coverage.
9. Difficult-case and counterexample search.
10. Actual tool execution must match reported execution.

## B. Adapt for AI-issued semantic judgments

1. Let AI create a versioned **preferred semantic conclusion**, not merely a proposal, when it attaches admissible evidence, alternatives, counterevidence, uncertainty, completeness and execution receipts. [TR-027]
2. Replace Lisan Internal Lock with a lighter decision policy that can allow a bounded conclusion while keeping unresolved risks visible.
3. Require server-owned deterministic validation of sources/occurrences/tool runs; let AI judge semantic fit above those facts.
4. Preserve an internal-analysis snapshot, then permit external comparison to revise the preferred conclusion with a visible change/influence record.
5. Store semantic decision rationale (concise reviewable reasons), not hidden chain-of-thought.

## C. Restrictions not to carry over

1. AI proposal-only as an absolute rule.
2. Mandatory eight-dimension Purity + Internal Lock as one gate before any semantic conclusion.
3. Publication/review/freshness lifecycle attached to every research result.
4. Steward authority and owner-acceptance fields in semantic method artifacts.
5. Mandatory ceremony when only one serious hypothesis or neighbor exists.
6. Fixed multi-phase release verification for exploratory research.

## D. Missing capabilities to introduce

1. First-class lexical-unit and branch identity.
2. Token/segment structural corpus with exact provenance and ambiguity.
3. Evidence and counterevidence relation objects, not opaque reference lists.
4. Executed completeness computation with denominators and exclusions.
5. AI semantic-decision record and revision/influence lineage.
6. Multidimensional semantic-distance representation distinct from vector similarity.
7. Calibrated result-strength research program.
8. Explicit independence classes and blind-verification protocol.
9. Pretrained-exposure risk declaration and contamination challenge tests.
10. `NO_DISTINCTION_ESTABLISHED` and typed unresolved outcomes.

## Minimum viable root-concept experiment

Use one medium-size root with known form/construction diversity and one close neighbor. Build exact occurrences plus minimal token morphology, run two internally isolated hypothesis/falsification cycles, perform a held-out challenge, then open one external comparison source and record any revision. Evaluate whether the AI can issue a reviewable preference without conflating layers—not whether it reproduces a traditional definition. [TR-028]
