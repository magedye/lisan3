# Confidence, Evaluation and Falsification

## Three independent measures

The new project’s proposed separation is well founded:

1. **Semantic result strength:** how well the conclusion is supported, discriminating, falsifiable and robust to counterevidence.
2. **Research completeness:** how much of the declared evidence/search space was actually collected, analyzed and challenged.
3. **Independent verification:** what separately configured reviewer reproduced or challenged the result under a declared independence class.

None can substitute for another. A strong result can be incomplete; a complete study can remain equivocal; two correlated agents can agree without independence. [TR-090]

## What Lisan3 already contains

| Concern | Existing material | Limitation |
|---|---|---|
| Evidence strength | Supporting evidence, counterevidence, unresolved cases, neighbor tests, rejection condition | No calibrated aggregate model; evidence mostly opaque refs |
| Confidence | Skill warns against uncalibrated percentages; legacy cards have confidence fields | Terms/levels are not consistently governed or empirically calibrated |
| Coverage/completeness | Skill separates index, deep, form, construction, context, neighbor and unresolved | Current persisted claim only has two free-text coverage fields; `QualityProfile` has scalars without validated semantics |
| Falsification | Detailed condition contract and test battery | Current code validates shape; execution receipts are not first-class |
| Purity | Eight detailed canonical evidence contracts | Current evaluator implements only a timestamp heuristic for Dictionary-First; seven dimensions are `NOT_EVALUATED` |
| Independent verification | Candidate-bound review discipline and Blind Lab concept | Mostly engineering/governance review, not calibrated independent semantic replication |
| Reproducibility | Corpus/method hashes, AI records, manifests, vector config hashes | Current run manifest endpoint includes static/simulated tool/model claims and says exact AI replay is unavailable |

## Candidate semantic-strength components

Do not finalize weights yet. Measure components separately first: [TR-091]

- `source_integrity`: all decisive premises resolve to permitted sources;
- `evidence_directness`: observation versus derived interpretation/external comparison;
- `coverage_relevance`: decisive strata represented, distinct from completeness total;
- `layer_attribution_stability`: alternatives controlled;
- `discrimination`: essential neighbors/negative cases separated;
- `predictive_success`: predeclared predictions surviving held-out cases;
- `falsification_survival`: operational challenges executed and survived;
- `counterevidence_burden`: unresolved severity and scope;
- `branch_stability`: result survives plausible lexical-unit partitions;
- `reasoning_reproducibility`: repeated decision under controlled configuration;
- `contamination_risk`: detected/suspected/unknown source influence;
- `calibration_evidence`: historical accuracy on labeled cases, if available.

Recommended initial output: component states (`STRONG`, `MODERATE`, `WEAK`, `NOT_EVALUATED`) plus evidence refs and an overall ordinal judgment with an explicit rule. Avoid percentages until calibration shows what they mean.

## Candidate completeness components

- corpus snapshot and query identity verified;
- index coverage numerator/denominator;
- deep-analysis coverage;
- form/derivation strata;
- construction strata;
- participant-role diversity;
- context-cluster diversity;
- difficult/outlier cases;
- essential-neighbor coverage;
- alternative-hypothesis coverage;
- rejection-condition execution;
- external-comparison coverage, if in scope;
- unresolved/excluded items and reasons;
- sampling and generalization boundary.

Completeness must never increase merely because the model emits more prose. [TR-092]

## Independent verification

Record:

- verifier identity and independence class;
- model/provider/config and whether it differs;
- evidence available/hidden;
- protocol revision;
- holdout/challenge set;
- decision and component ratings;
- disagreements and their resolution status;
- exact artifact hashes.

A same-model adversarial Agent can count as `CONTEXT_BLIND_REVIEW`, not automatically `MODEL_FAMILY_INDEPENDENT`. [TR-093]

## Falsification protocol

1. Freeze the hypothesis statement/scope and predictions.
2. Validate that rejection trigger is observable and non-circular.
3. Declare search space, method and confound controls.
4. Search hardest occurrences, rare forms, outliers and closest neighbors.
5. Record all inspected cases and execution receipts.
6. Apply the predeclared consequence: reject, narrow, split, reopen or retain.
7. Preserve failed predictions and unresolved cases in the decision.
8. Rerun strength and completeness components after revision.

This separates “we wrote a rejection condition” from “we tried to falsify the claim.” [TR-094]

## Purity lessons to retain and discard

Retain individual diagnostics: Dictionary-First, Contextual Leakage, Heritage Bias, Tafsir Contamination, Forced Unification, Generic Overextraction, Letter-Semantics Overreliance and Circular Confirmation. Each describes a real methodological failure class. [TR-095]

Discard the assumption that all eight must be a single monolithic gate before AI can state any bounded conclusion. For the new project, each diagnostic should affect source integrity, result strength, completeness or required warnings according to actual evidence. Critical fabricated-source/tool-use failures may invalidate a result; a not-yet-run optional heritage comparison should not. [TR-096]

## Calibration experiments

1. Build synthetic and expert-labeled cases for each failure class.
2. Collect AI component ratings before revealing labels.
3. Measure discrimination/calibration and common inflation.
4. Compare self-rating, rule-derived rating and independent review.
5. Test whether component evidence predicts later rejection/revision.
6. Only then consider weights or numeric probabilities.

No repository evidence supports final weights today. [TR-097]

## Fail-closed conditions

Regardless of higher AI authority, the result should be invalid or explicitly non-evidential when:

- decisive Quran citation/source identity is fabricated or unresolved;
- a claimed Tool execution has no authoritative receipt;
- external/traditional content is labeled Quran-internal evidence;
- evidence relations are circular with no independent terminal evidence;
- target/analysis unit cannot be resolved;
- conclusion exceeds its declared scope;
- critical counterevidence is removed or concealed.

Other incompleteness should lower completeness/strength or preserve alternatives rather than always blocking all output. [TR-098]
