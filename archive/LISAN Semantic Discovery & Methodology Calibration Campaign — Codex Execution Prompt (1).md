# LISAN3 — Large-Scale Semantic Discovery & Methodology Calibration Campaign

## Mission

Work directly on the LISAN3 repository.

Design, implement, qualify, and then execute a persistent large-scale Quranic semantic research campaign whose purpose is simultaneously to:

1. apply the active **Lisan Quran methodology** rigorously to as many eligible Quranic roots as possible;
2. produce durable, traceable root research results;
3. identify obstacles, methodological weaknesses, unnecessary constraints, ambiguities, recurrent failure modes, and unexpected insights revealed by real use;
4. convert those observations into structured methodology-improvement proposals;
5. progressively build a database of accepted root concepts and semantic outputs;
6. build a growing semantic evaluation/regression suite from difficult and informative cases;
7. generate cross-root research hypotheses that may reveal additional semantic, morphological, constructional, and conceptual regularities.

This is not a documentation-only task.

This is a:

**Inspect → Design → Implement → Qualify → Calibrate → Execute → Learn → Scale**

task.

Do not merely provide recommendations.

Do not attempt to process hundreds of roots before the campaign infrastructure and calibration batch have been qualified.

---

# 1. Owner intent

The owner wants the largest practical number of Quranic roots to be researched, but:

> qualified semantic results are more important than raw root count.

Therefore optimize for:

**maximum number of methodologically qualified roots**

not:

**maximum number of generated answers.**

The campaign must be resumable.

Do not rely on one long model context.

Persist campaign state after every root.

---

# 2. Governing methodology

Use the currently active, owner-authorized Lisan Quran methodology and semantic runtime contracts.

Do not create a competing methodology.

Preserve the fundamental methodology:

```text
Root contribution
↓
general derivation / inflection contribution
↓
lexeme in relation to its root
↓
general morphological-form contribution
↓
general construction contribution
↓
form contribution in the specific occurrence
↓
construction / participant-role contribution in the occurrence
↓
context / discourse contribution
↓
local meaning
↓
final semantic statement
```

Never attribute to the root what is better explained by:

- morphology,
- derivation,
- construction,
- participant roles,
- discourse,
- local context.

AI may perform semantic judgment and preference.

AI may not fabricate evidence or silently convert a research judgment into canonical project knowledge.

---

# 3. Preconditions

Before changing or executing anything:

## V0 — Baseline

Record:

- exact HEAD SHA;
- branch;
- worktree status;
- active methodology revision;
- active corpus snapshot;
- active semantic Skill;
- active source policy;
- structural/morphological source status;
- relevant tests;
- existing ResearchRun/SemanticClaim/Hypothesis/Gate infrastructure;
- whether the governance-simplification work requested by the owner has already been completed and verified.

Do not overwrite unrelated user work.

If governance simplification has not yet been implemented:

- do not silently redesign it in this task;
- run this campaign under the currently active authority;
- identify unnecessary campaign friction as Methodology/Governance Findings.

If a required root/morphology source is not sufficiently qualified for large-scale root inventory:

- do not infer root identities from model memory;
- record a scaling blocker;
- implement the smallest qualified root-inventory solution allowed by current project authority, or stop the dependent scale-out stage if doing so requires a separate owner decision.

---

# 4. Reuse existing domain structures

Prefer extending existing LISAN3 records rather than creating a parallel knowledge system.

Inspect and reuse where appropriate:

- `ResearchRun`
- `SemanticClaim`
- `Hypothesis`
- `ObservationArtifact`
- `GateReport`
- `AIExecutionRecord`
- evidence/provenance infrastructure
- corpus occurrences
- current methodology revision system

Add only campaign-specific records that have clear value.

At minimum evaluate the need for:

```text
ResearchCampaign
CampaignRoot
MethodologyFinding
ConfidenceAssessment
VerificationRun
AcceptedRootConcept
CrossRootInsight
```

Do not duplicate data already represented correctly elsewhere.

---

# 5. Campaign state

The campaign must be persistent and resumable.

Suggested lifecycle:

```text
CREATED
→ INVENTORY_BUILT
→ CALIBRATION_RUNNING
→ CALIBRATION_REVIEW
→ SCALE_READY
→ BATCH_RUNNING
→ BATCH_REVIEW
→ CONTINUE | PAUSED | COMPLETED
```

A process/session crash must not lose:

- completed root results;
- findings;
- evidence references;
- methodology revision;
- verification state;
- campaign queue.

---

# 6. Build the Root Universe

Construct the complete set of root candidates supported by qualified project data.

For every root candidate record at least:

```text
root
structural_identity_status
occurrence_count
derivational_family_size
morphological_form_diversity
construction_diversity
known_or_detected_lexical_ambiguity
semantic_neighbor_candidates
structural_data_reliability
research_eligibility
ineligibility_reason
```

Do not use LLM memory as the root inventory.

The inventory must be reproducible from admitted project data.

---

# 7. Root portfolio selection

Do not rank roots only by frequency.

Create a stratified portfolio using dimensions such as:

```text
occurrence volume
derivational diversity
morphological diversity
construction diversity
participant-role diversity
semantic-neighbor pressure
lexical ambiguity
structural-data reliability
expected research difficulty
```

The calibration set must deliberately include:

- easier roots;
- medium-complexity roots;
- difficult roots;
- low-frequency roots;
- high-frequency roots;
- roots with multiple forms;
- roots with close semantic neighbors;
- roots likely to expose layer-conflation errors;
- at least some roots where UNRESOLVED is a plausible correct result.

Avoid a homogeneous first batch.

---

# 8. Campaign scaling strategy

Use adaptive batches.

## Phase A — Calibration

Select approximately 8–12 highly diverse roots.

Freeze the methodology revision for the whole calibration batch.

Do not modify the canonical methodology midway through the batch.

Record every problem and lesson.

---

## Phase B — Batch review

After the calibration roots:

- compare all results;
- aggregate methodological findings;
- identify recurrent vs root-specific problems;
- propose methodology changes;
- identify false blockers and excessive procedural cost;
- identify missing data/tools/contracts;
- identify new evaluation cases.

Do not automatically adopt methodology changes.

Produce formal MethodologyChangeProposals.

---

## Phase C — Expansion

If the campaign and methodology are stable enough, run a larger batch, approximately 20–30 roots.

---

## Phase D — Scale

Move to batches around 50 roots or another size justified by measured execution cost and failure rate.

Continue processing eligible roots until one of the defined stop conditions occurs.

The campaign should be restartable and capable of processing additional batches later.

---

# 9. Methodology freeze rule

This rule is mandatory:

> A methodology revision is frozen for the duration of one research batch.

Methodology findings discovered during the batch are queued.

They do not silently alter later roots in the same batch.

If the owner or current project authority accepts a methodology revision after batch review:

1. create a new version;
2. preserve the previous version;
3. record the exact delta;
4. rerun methodology sentinel roots;
5. compare old vs new behavior;
6. check for semantic regression;
7. only then use the new methodology for subsequent batches.

---

# 10. Per-root research protocol

For each eligible root, execute the active Lisan methodology fully.

At minimum:

## A. Root identity

Resolve:

- root;
- lexical-unit ambiguity;
- derivational family;
- admitted structural evidence.

---

## B. Full occurrence inventory

Retrieve all eligible occurrences.

Prove index coverage deterministically.

Record exclusions and ambiguity.

---

## C. Structural distribution

Analyze:

- forms;
- derivations;
- constructions;
- particles/prepositions;
- participants;
- semantic roles;
- discourse/context clusters.

---

## D. Observation phase

Separate direct observations from interpretation.

Do not begin with a final root meaning.

---

## E. Hypothesis generation

Generate more than one serious root-concept hypothesis when warranted.

Always permit:

```text
C0 = no unified root concept established
```

and:

```text
multiple lexical units
```

where evidence supports them.

---

## F. Root concept extraction

Ask:

> What is the minimum semantic structure that must be attributed to the root in order to explain its contribution across its derivations and occurrences after subtracting what is better explained by morphology, construction, and context?

The candidate should be:

- shared;
- stable;
- sufficiently abstract;
- non-vacuous;
- distinctive where evidence permits;
- economical;
- explanatory;
- falsifiable;
- non-circular.

---

## G. Semantic boundary

Record:

```text
REQUIRED
PERMITTED
EXCLUDED
UNKNOWN
LOCAL_REALIZATION
```

Do not fill UNKNOWN by intuition.

---

## H. Semantic neighbors

Identify serious nearby roots/lexemes.

For each relevant neighbor examine:

```text
shared semantic domain
target-specific features
neighbor-specific features
construction distribution
context distribution
participant roles
counterfactual substitution
what is lost or changed
unresolved dimensions
```

Counterfactual substitution is exploratory evidence only, never independent proof.

---

## I. Falsification

For every serious preferred hypothesis identify:

```text
strongest counterexample
strongest competitor
weakening conditions
rejection conditions
failed predictions
unresolved cases
reopen conditions
```

Actively try to defeat the hypothesis.

Do not merely collect support.

---

## J. Holdout validation

Where the occurrence set permits it:

withhold some occurrences or context clusters from initial hypothesis construction.

Freeze the hypothesis.

Then test it against the held-out material.

Store the result.

Do not retroactively rewrite the original hypothesis without recording revision lineage.

---

## K. Final semantic judgment

Produce one of:

```text
PREFERRED_ROOT_CONCEPT
MULTIPLE_LEXICAL_UNITS
UNRESOLVED
INSUFFICIENT_EVIDENCE
REJECTED_HYPOTHESIS
```

Do not force a single meaning.

---

# 11. Required Semantic Derivation Chain

For important representative lexemes/occurrences within every root, preserve:

```text
root contribution
→ general derivation/inflection contribution
→ lexeme-root relation
→ general form contribution
→ general construction contribution
→ specific form contribution
→ specific construction and participant roles
→ context/discourse contribution
→ local meaning
→ final semantic statement
```

This chain must be inspectable.

Use it to detect layer-conflation.

---

# 12. Confidence model

Do not use model self-confidence.

Do not invent an uncalibrated percentage.

For every result generate a `ConfidenceAssessment` with at least:

```text
coverage_adequacy
structural_data_reliability
cross_occurrence_consistency
derivational_consistency
layer_separation_quality
semantic_neighbor_differentiation
counterevidence_burden
falsification_survival
holdout_performance
independent_verification
unresolved_materiality
```

Store:

```text
overall_strength:
  STRONG | MODERATE | WEAK | UNRESOLVED
```

and:

```text
confidence_rationale
```

The rationale must explain why the classification was assigned.

Do not average component values into a probability unless an approved calibration system exists.

---

# 13. Confidence-improvement experiments

Where practical, execute or schedule the following experiments.

## Held-out occurrence test

Test the concept against unseen occurrences.

## Leave-cluster-out test

Withhold an entire contextual/form/construction cluster where feasible.

## Occurrence-order sensitivity

Repeat analysis with materially different occurrence ordering.

If the preferred concept changes substantially, record robustness risk.

## Blind adversarial verification

A verifier that does not see the preferred conclusion first attempts independent analysis/challenge.

## Model diversity test

If another qualified model/provider is available, use it as a robustness check.

Agreement is not semantic evidence.

## Neighbor challenge

Force the preferred concept to distinguish itself from the strongest neighbor.

## Prediction test

Before revealing held-out cases, record predictions implied by the preferred root concept and evaluate them afterward.

## Methodology sentinel roots

Maintain a fixed set of representative roots that are rerun after methodology revisions.

---

# 14. Methodology learning loop

Every root research run may produce zero or more `MethodologyFinding` records.

Use categories such as:

```text
METHOD_GAP
METHOD_AMBIGUITY
METHOD_OVERCONSTRAINT
METHOD_UNDERSPECIFICATION
FALSE_BLOCKER
DATA_GAP
SOURCE_GAP
TOOL_GAP
SCHEMA_GAP
OUTPUT_GAP
CONFIDENCE_GAP
LAYER_CONFLATION_RISK
COVERAGE_COST
PERFORMANCE_COST
RECURRING_FAILURE
UNEXPECTED_INSIGHT
```

Each finding must contain:

```text
finding_id
root
research_run_id
methodology_revision
category
description
reproduction_evidence
affected_stage
affected_claim_type
severity
frequency_so_far
root_specific_or_general
current_workaround
proposed_fix
expected_value
expected_cost
risk_of_change
```

---

# 15. Representing methodology improvements

For every generalizable finding, propose the smallest appropriate representation.

Choose one of:

```text
CONSTITUTIONAL_PRINCIPLE
METHODOLOGY_RULE
CONTROL
SKILL_STEP
TOOL
VALIDATOR
GATE
SCHEMA_FIELD
OUTPUT_CONTRACT
EVAL_CASE
EXAMPLE
DOCUMENTATION_CLARIFICATION
NO_CHANGE
```

Important:

Do not propose a `Gate` unless actual fail-closed enforcement is necessary.

Do not propose a constitutional principle for a local implementation problem.

Prefer the lightest mechanism that prevents the observed failure.

Each proposal must explain:

```text
why this representation is appropriate
why a lighter mechanism is insufficient
how much complexity it adds
what measured failure it prevents
```

---

# 16. Do not self-modify methodology silently

The campaign may:

- discover findings;
- aggregate evidence;
- propose changes;
- implement campaign tooling;
- add eval cases.

The campaign must not silently rewrite canonical semantic methodology in response to a single root.

Methodology change requires a separate accepted revision under current project authority.

---

# 17. Accepted Root Concept Memory

Create or extend a durable accepted-result mechanism.

Do not store every hypothesis as accepted knowledge.

A root result may enter accepted root memory only when:

```text
result_strength == STRONG
AND required coverage is satisfied
AND falsification completed
AND material counterevidence is resolved or explicitly bounded
AND layer separation is reviewable
AND required independent verification is satisfied
AND project acceptance policy is satisfied
```

If confidence percentages are not calibrated:

do not require an arbitrary numerical threshold.

Use:

```text
STRONG + ACCEPTED
```

Store at least:

```text
root
root_concept
plain_explanation

required_features
permitted_features
excluded_features
unknown_features

derivational_family_summary
important_form_contributions
important_construction_contributions

semantic_neighbors
distinctive_features

hard_cases
strongest_counterexample
strongest_competitor

result_strength
confidence_rationale
research_completeness
independent_verification

methodology_revision
corpus_snapshot
research_run_id
accepted_result_revision
accepted_at
accepted_by

reopen_conditions
supersedes
```

Never silently overwrite an accepted result.

A materially new challenge creates a new research revision.

---

# 18. Research database views

Provide queryable views/reports for at least:

```text
all researched roots
accepted roots
strong but not accepted roots
moderate roots
unresolved roots
roots blocked by data
roots with serious counterevidence
roots with methodology findings
roots requiring revalidation
roots by methodology revision
roots by confidence dimension
```

---

# 19. Convert hard cases into evaluation assets

Whenever a root exposes a meaningful failure:

turn the smallest reproducible case into a semantic regression test where appropriate.

Examples:

```text
root/context conflation
root/form conflation
invented semantic distinction
hidden external contamination
false completeness
failure to preserve UNRESOLVED
missed counterexample
incorrect root identity
unsupported tool claim
unstable result under occurrence order
accepted-result memory misuse
```

The evaluation suite should grow as the campaign grows.

---

# 20. Cross-root insight discovery

After a sufficient number of roots have been researched, perform periodic cross-root analysis.

Look for candidate patterns involving:

```text
morphological operator contributions
derivational behavior
construction semantics
preposition interactions
participant-role patterns
semantic-neighbor dimensions
discourse functions
root-to-local-meaning transformations
recurring semantic boundaries
recurring failure modes
```

Store these as:

```text
CrossRootInsight
```

with status:

```text
CANDIDATE
TESTED
SUPPORTED
REJECTED
UNRESOLVED
```

Do not convert cross-root patterns directly into methodology rules or semantic truth.

They require their own evidence and falsification.

---

# 21. Additional meaning-discovery opportunities

Use the campaign to generate research queues for:

- morphological-form induction across multiple roots;
- construction-level semantic induction;
- semantic-neighbor maps;
- semantic dimensions distinguishing near terms;
- lexical-unit splitting candidates;
- recurring context effects;
- discourse-function clusters;
- anomalous occurrences;
- roots whose accepted concept predicts new local-meaning distinctions.

These are research candidates, not automatic conclusions.

---

# 22. Root prioritization after calibration

After the calibration batch, prioritize subsequent roots using **information value**, not frequency alone.

Prefer roots that either:

1. can produce useful reusable accepted knowledge; or
2. strongly test a weak point in the methodology.

Maintain diversity.

Do not process only easy roots to maximize success rate.

Do not process only hard roots to maximize findings.

---

# 23. Throughput metrics

Track campaign productivity.

At minimum:

```text
eligible_roots
researched_roots
accepted_roots
strong_results
moderate_results
unresolved_results
blocked_roots

average_occurrences_per_root
average_runtime_or_execution_cost_per_root

findings_per_root
generalizable_findings
new_eval_cases

falsification_failure_rate
holdout_failure_rate
independent_verification_disagreement_rate

methodology_regressions_detected
```

Do not optimize for accepted-root count alone.

---

# 24. Root result artifact

Produce a complete `RootResearchArtifact` for each researched root.

It must include:

1. research identity;
2. root identity and scope;
3. occurrence/derivational coverage;
4. observations;
5. competing hypotheses;
6. preferred root concept or unresolved result;
7. semantic boundary;
8. morphological analysis;
9. construction analysis;
10. decisive contexts;
11. semantic-neighbor analysis;
12. representative local-meaning derivation chains;
13. strongest evidence;
14. strongest counterevidence;
15. falsification;
16. holdout results where available;
17. confidence assessment;
18. independent verification;
19. methodology findings;
20. reopen conditions;
21. provenance.

A short `RootCard` may be derived from this artifact.

The card must not create new knowledge.

---

# 25. Failure discipline

A root research run may end legitimately as:

```text
UNRESOLVED
INSUFFICIENT_EVIDENCE
DATA_BLOCKED
STRUCTURAL_IDENTITY_UNCERTAIN
METHODOLOGY_BLOCKED
```

Do not convert these to failed campaign execution unless the runtime itself malfunctioned.

These states are research data.

---

# 26. Campaign stop conditions

Continue processing roots until one of the following occurs:

1. all eligible queued roots for the current campaign scope are processed;
2. a general methodology defect makes a large class of further results unreliable;
3. the admitted structural/root source proves unsuitable for scaling;
4. infrastructure failure prevents traceable research;
5. the remaining roots are ineligible under current data quality;
6. explicit owner stop.

Do not stop simply because several roots are UNRESOLVED.

Do not silently lower standards to increase root count.

---

# 27. Checkpointing

After every root:

- persist all records;
- update campaign status;
- update queue;
- write execution evidence;
- ensure the root can be reconstructed without model memory.

After every batch:

- produce a batch report;
- aggregate methodology findings;
- update eval candidates;
- calculate campaign metrics;
- identify next portfolio.

---

# 28. No unrelated redesign

Do not use this campaign to redesign:

- UI;
- unrelated backend modules;
- authentication;
- multi-user architecture;
- publication system;
- vector/graph infrastructure;
- external-source policy;
- Quran corpus identity.

Make only changes necessary for the campaign, persistence, testing, and result retrieval.

Preserve unrelated user work.

---

# 29. Git discipline

- Record exact base SHA.
- Do not reset unrelated changes.
- Do not clean user files.
- Do not push.
- Do not merge.
- Do not tag.
- Do not release unless separately authorized.

Commit only if the current owner/project instructions authorize local commits; otherwise leave a clear candidate worktree.

---

# 30. Required initial deliverables before large-scale execution

Before processing more than the calibration batch, produce and validate:

```text
SEMANTIC_CAMPAIGN_ARCHITECTURE.md
ROOT_UNIVERSE_REPORT.md
ROOT_SELECTION_STRATEGY.md
CAMPAIGN_DATA_CONTRACT.md
METHODOLOGY_FINDING_CONTRACT.md
CONFIDENCE_ASSESSMENT_CONTRACT.md
ACCEPTED_ROOT_MEMORY_CONTRACT.md
SEMANTIC_CAMPAIGN_TEST_PLAN.md
```

Plus executable migrations/contracts/tests required by the implementation.

Do not stop after creating these documents.

Qualify them and run the calibration batch.

---

# 31. Calibration acceptance

The campaign may scale only if the calibration batch demonstrates:

- correct source isolation;
- reproducible root inventory;
- complete index coverage where claimed;
- correct layer separation;
- serious competing hypotheses;
- falsification actually executed;
- counterevidence retained;
- UNRESOLVED preserved;
- confidence rationale produced;
- root artifacts persisted;
- methodology findings persisted;
- restart/resume works;
- accepted-memory rules do not accidentally promote weak results.

If not, fix campaign infrastructure or report the blocker before scaling.

---

# 32. Final report for each batch

Return:

1. exact repository identity;
2. methodology revision;
3. corpus snapshot;
4. batch identifier;
5. selected roots and why;
6. completed roots;
7. accepted/strong/moderate/unresolved/blocked counts;
8. root-result table;
9. confidence summaries;
10. strongest discoveries;
11. strongest counterexamples;
12. methodology findings;
13. repeated findings across roots;
14. proposed methodology changes and representation type;
15. new semantic eval cases;
16. cross-root insight candidates;
17. confidence-improvement opportunities;
18. additional semantic-discovery opportunities;
19. campaign throughput/cost observations;
20. blockers;
21. next recommended root portfolio;
22. files/schema/code changed;
23. tests executed and exact results;
24. unrelated files confirmed untouched.

---

# 33. Final campaign objective

The desired end state is not merely a directory of AI answers.

The desired end state is:

```text
Qualified Quranic Root Inventory
        +
Traceable Root Research Database
        +
Accepted Root Concept Memory
        +
Confidence & Verification Profiles
        +
Counterevidence / Hard-Case Database
        +
Semantic Regression Suite
        +
Methodology Learning Register
        +
Cross-Root Research Queue
```

The campaign is successful when the project can answer:

> What do we currently believe this root contributes semantically?

and also:

> Why do we believe it?

> What evidence challenges it?

> How complete was the research?

> How strong is the result and why?

> Which methodology revision produced it?

> What would cause us to reopen it?

> What did researching this root teach us about the methodology itself?

Process the largest practical number of **qualified** roots, but never trade traceability, falsifiability, layer separation, or evidence integrity for raw throughput.