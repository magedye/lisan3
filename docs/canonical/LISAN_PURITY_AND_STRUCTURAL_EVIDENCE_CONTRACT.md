# Lisan Purity and Structural Evidence Contract

Authority revision: `LISAN3_PURITY_STRUCTURAL_CONTRACT_V2_2026_08_27`

## Purpose and current boundary

This contract removes implementation ambiguity for the eight mandatory Purity
dimensions and for a future auxiliary structural annotation layer. It does not
admit or activate QAC, implement an importer or evaluator, rerun a ResearchRun,
or establish semantic truth.

The current evaluator implements only a partial temporal check for
`DICTIONARY_FIRST`; the other seven dimensions are unsupported. A dimension is
not complete merely because its implementation can be written before morphology
is admitted. It can return `EVALUATED_CLEAN` only when the required evidence for
the evaluated subject is present, source-bound, and complete.

## Mandatory fail-closed result contract

Each dimension must emit exactly one current result state:

- `EVALUATED_CLEAN`: every mandatory input is present, lineage is resolvable,
  coverage is complete for the evaluation subject, and the clean rule passes;
- `FLAGGED`: evidence proves the prohibited failure mode or a mandatory
  invariant fails;
- `NOT_EVALUATED`: a mandatory input, lineage edge, supported extractor, or
  required coverage proof is absent or ambiguous.

`NOT_EVALUATED` is never equivalent to `EVALUATED_CLEAN`. Every non-clean result
blocks `PURITY_CHECK`. A score or aggregate rating cannot override a non-clean
dimension.

Every finding must diagnose at least: `dimension`, `status`, `severity`,
`details`, evaluated subject and revision, evidence references, source and
artifact lineage, missing inputs, and the deterministic rule/version applied.
The present `PurityFinding` response and persisted JSON do not yet express all
of these fields; that is an implementation gap, not permission to omit them.

## Evidence admissibility common to all dimensions

Acceptable inputs are governed records bound to the same ResearchRun and exact
revisions: admitted CorpusSnapshot/occurrence evidence, ObservationArtifact,
Hypothesis, SemanticClaim, EssentialNeighbor, GateReport, IsolationState,
IsolationEvent, access/audit events, DependencyRecord, and explicitly admitted
source manifests. Derived cards, UI projections, AI output, unbound free text,
fixtures, and model memory cannot establish a clean result.

Evidence references must resolve to immutable or revision-bound records and
carry the ResearchRun, corpus snapshot, methodology revision, source role,
artifact identity/hash where applicable, creator/process identity, and event
time. Missing or cross-run lineage is `NOT_EVALUATED`; prohibited-source use is
`FLAGGED`.

## Dependency matrix

| Dimension | Required inputs | Morphology dependency | Implementable now? | Missing capability | Minimum required tests |
|---|---|---|---|---|---|
| `DICTIONARY_FIRST` | observations, hypotheses, access/audit chronology, source roles | None | Substantially; current timestamp-only check is incomplete | governed access lineage and completeness proof | ordered clean, hypothesis-first, forbidden access, missing chronology |
| `CONTEXTUAL_LEAKAGE` | occurrence-scoped observations, authorized context window, access/isolation events | Material for final coverage | Partially | token/segment/root alignment and context-window provenance | in-window clean, cross-window leak, ambiguous boundary, missing alignment |
| `HERITAGE_BIAS` | hypotheses/claims, heritage-source manifest, access events, internal evidence lineage | None | Yes | source classification and claim-to-source dependency extraction | no-access clean, premature heritage use, unresolved source role, paraphrase leak |
| `TAFSIR_CONTAMINATION` | hypotheses/claims, tafsir manifest, access/isolation events, content lineage | None | Yes | source classification and dependency extraction | no-access clean, direct/indirect tafsir use, blocked attempt, missing logs |
| `FORCED_UNIFICATION` | complete occurrence groups, observations, hypotheses, counterevidence, unresolved branches | Material | Contract logic only before structural data | exact occurrence/root/form coverage and grouping | justified unity, distinct-cluster coercion, unresolved exception, incomplete coverage |
| `GENERIC_OVEREXTRACTION` | hypothesis/claim scope, observations, neighbor probes, counterexamples, rejection condition | None for evaluator; governed occurrence evidence still required at runtime | Yes | normalized scope and probe-result contract | bounded clean, generic claim, failed neighbor test, absent falsification |
| `LETTER_SEMANTICS_OVERRELIANCE` | hypothesis/claim rationale, evidence refs, dependency graph, corpus observations | None | Yes | rationale/dependency classification | corpus-grounded clean, letter-only inference, mixed unsupported inference, missing rationale |
| `CIRCULAR_CONFIRMATION` | hypotheses/claims, evidence/counterevidence refs, dependency graph, derivation lineage | None | Yes | typed derivation edges and cycle detection | acyclic support, direct cycle, transitive cycle, unresolved reference |

The morphology-independent implementation set is `DICTIONARY_FIRST`,
`HERITAGE_BIAS`, `TAFSIR_CONTAMINATION`, `GENERIC_OVEREXTRACTION`,
`LETTER_SEMANTICS_OVERRELIANCE`, and `CIRCULAR_CONFIRMATION`.
`CONTEXTUAL_LEAKAGE` can gain access-policy checks before morphology but cannot
prove final clean coverage without structural alignment. `FORCED_UNIFICATION`
materially depends on complete structural occurrence grouping.

## DICTIONARY_FIRST

- **Purpose:** prove that Quran-internal observation precedes hypothesis
  formation and exposure to dictionary-derived semantic content.
- **Prohibited failure mode:** a hypothesis or semantic frame is formed from a
  dictionary before the required corpus observations, then projected onto them.
- **Mandatory inputs:** complete ordered ObservationArtifact and Hypothesis
  events; access/audit events; source-role manifest; ResearchRun, corpus, and
  methodology revisions.
- **Acceptable evidence sources:** same-run observation/hypothesis records and
  enforced access events; admitted source manifests only for source
  classification.
- **Lineage:** every timestamped event resolves to the run and revision, and the
  access log proves relevant access coverage rather than mere absence in a
  partial log.
- **Decision rule:** order the authoritative event stream. Flag if a hypothesis
  or dictionary-semantic access precedes required internal observations. Clean
  only when observations precede hypotheses and no prohibited early access is
  present in a complete log.
- **Clean:** ordered internal observation first, complete access record, no
  early dictionary-derived semantic dependency.
- **Failed:** hypothesis-first ordering or proven early dictionary use.
- **NOT_EVALUATED:** missing observation, hypothesis, trustworthy chronology,
  source classification, or log-completeness evidence.
- **Diagnostics:** first observation/hypothesis/access references and times,
  offending source/action, missing chronology fields, rule revision.
- **Morphology/root required:** no.
- **Before QAC:** yes; replace the current timestamp-only heuristic with this
  contract, while incomplete runs remain `NOT_EVALUATED`.
- **Fixtures and negative tests:** clean ordered run; equal-time deterministic
  tie-break; hypothesis-first run; early direct and indirect dictionary access;
  absent/incomplete access log.
- **Dependencies and level:** observations, hypotheses, access/audit and
  isolation events; run-level with hypothesis-level offending references.

## CONTEXTUAL_LEAKAGE

- **Purpose:** prove that an observation or hypothesis uses only its authorized
  Quranic context and does not import evidence from hidden, neighboring,
  cross-root, later-stage, or prohibited contexts.
- **Prohibited failure mode:** contextual material outside the declared
  occurrence/window or stage influences the result without an authorized,
  traceable dependency.
- **Mandatory inputs:** exact occurrence and token/segment locators, declared
  context-window policy, observation-to-occurrence links, access/isolation
  events, hypotheses/claims, corpus and methodology revisions.
- **Acceptable evidence sources:** Tanzil text/verse identity, an admitted
  structural annotation layer, same-run observations, and enforced access logs.
- **Lineage:** every accessed span resolves to the exact snapshot, verse,
  word/segment, stage, action, and resulting artifact.
- **Decision rule:** compare all reads and dependencies with the authorized
  context set for each artifact. Any unapproved out-of-window influence flags;
  all reads must be classified for clean.
- **Clean:** complete structural/access coverage and every dependency is within
  policy or explicitly authorized for that stage.
- **Failed:** proven unapproved cross-context, cross-run, hidden-result, or
  later-stage leakage.
- **NOT_EVALUATED:** missing token/segment alignment, window policy, access
  completeness, or artifact-to-read lineage.
- **Diagnostics:** artifact, accessed locator, allowed window, violated rule,
  access/isolation event, and unresolved ranges.
- **Morphology/root required:** materially yes for exact root-occurrence and
  segment coverage; coarse access violations can be detected without it.
- **Before QAC:** partial access-policy evaluator only; final clean is not
  available for the pilot until admitted structural evidence exists.
- **Fixtures and negative tests:** fully in-window case; adjacent verse/segment
  leak; cross-root and cross-run reads; hidden prior result; ambiguous segment;
  incomplete access log.
- **Dependencies and level:** occurrences, observations, hypotheses/claims,
  isolation/access events; mixed occurrence-, artifact-, and run-level.

## HERITAGE_BIAS

- **Purpose:** detect inherited lexical or scholarly framing that substitutes
  for Quran-internal derivation.
- **Prohibited failure mode:** a heritage source supplies the hypothesis,
  boundary, or conclusion before internal lock, including unattributed
  paraphrase.
- **Mandatory inputs:** hypothesis/claim text and rationale, evidence refs,
  heritage-source role manifest, access/isolation events, derivation lineage,
  and stage chronology.
- **Acceptable evidence sources:** governed hypothesis/claim records, internal
  observations, source manifests, and enforced access logs. Heritage material
  may be evaluated only in a canonically permitted later comparison stage.
- **Lineage:** each external phrase/reference maps to a classified source,
  access event, stage, and dependent artifact.
- **Decision rule:** trace claim/hypothesis dependencies and access events. Flag
  any pre-lock heritage influence; a permitted post-lock comparison cannot
  retroactively support the internal derivation.
- **Clean:** complete logs show no pre-lock heritage influence and internal
  evidence independently supports the artifact.
- **Failed:** direct, indirect, copied, or paraphrased heritage framing influences
  a pre-lock artifact.
- **NOT_EVALUATED:** incomplete source inventory, logs, rationale, or dependency
  extraction.
- **Diagnostics:** source classification, phrase/dependency match, event/stage,
  affected artifact, and missing inventory.
- **Morphology/root required:** no.
- **Before QAC:** yes.
- **Fixtures and negative tests:** isolated internal run; direct early heritage
  access; unattributed paraphrase; permitted post-lock comparison; unknown
  source; incomplete access log.
- **Dependencies and level:** hypotheses, claims, observations, source/access/
  isolation events; mixed hypothesis-, claim-, and run-level.

## TAFSIR_CONTAMINATION

- **Purpose:** preserve Quran-internal analysis from prior tafsir conclusions.
- **Prohibited failure mode:** tafsir content, paraphrase, label, or conclusion
  enters observations, hypotheses, or claims before the permitted comparison
  boundary.
- **Mandatory inputs:** hypotheses/claims and rationale, evidence refs, tafsir
  source manifest, access/isolation events, content dependency lineage, and
  stage chronology.
- **Acceptable evidence sources:** governed internal artifacts and enforced
  access records; tafsir only where a later stage explicitly permits comparison.
- **Lineage:** exact source/work/reference, access action, stage, dependent
  artifact, and corpus/methodology revisions.
- **Decision rule:** classify all external dependencies and reads. Any pre-lock
  tafsir influence flags. A blocked attempt with no content disclosure proves
  enforcement and does not itself contaminate.
- **Clean:** complete logs and dependencies show no disclosed pre-lock tafsir
  content and no tafsir-derived artifact.
- **Failed:** direct/indirect tafsir content influences an internal artifact.
- **NOT_EVALUATED:** incomplete logs, unknown source classification, missing
  rationale, or unresolved dependency.
- **Diagnostics:** tafsir source/reference, access outcome, stage, affected
  artifact, match basis, and blocked-versus-disclosed distinction.
- **Morphology/root required:** no.
- **Before QAC:** yes.
- **Fixtures and negative tests:** no-access clean; blocked attempt clean;
  disclosed direct quote/reference; paraphrased conclusion; post-lock permitted
  comparison; missing source/log.
- **Dependencies and level:** observations, hypotheses, claims, access/audit and
  isolation events; mixed hypothesis-, claim-, and run-level.

## FORCED_UNIFICATION

- **Purpose:** prevent materially different occurrence patterns from being
  coerced into one Root Core or hypothesis.
- **Prohibited failure mode:** exceptions, distinct constructions, polysemy
  candidates, or participant differences are erased to preserve a single core.
- **Mandatory inputs:** complete root-occurrence inventory; token/segment, lemma,
  form, features and permitted syntax; observations; grouping rationale;
  hypotheses; counterevidence; unresolved branches; rejection conditions.
- **Acceptable evidence sources:** Tanzil-bound admitted structural annotations
  and governed same-run artifacts.
- **Lineage:** each group and exception resolves to exact occurrences and source
  annotations; claimed inventory completeness resolves to snapshot/hash.
- **Decision rule:** compare proposed unity against structurally/contextually
  distinct clusters. Flag when a materially supported cluster is discarded or
  relabeled without evidence. Preserve unresolved branches rather than force a
  pass.
- **Clean:** complete coverage; every material cluster is explained by tested
  shared constraints or explicitly retained as unresolved/counterevidence.
- **Failed:** coercion, silent exception removal, circular relabeling, or a
  universal claim contradicted by a material cluster.
- **NOT_EVALUATED:** incomplete occurrence coverage, absent structural fields,
  missing grouping rationale/counterevidence, or unresolved alignment.
- **Diagnostics:** cluster memberships, structural contrasts, excluded cases,
  hypothesis/rejection references, coverage counts, unresolved branches.
- **Morphology/root required:** materially yes.
- **Before QAC:** contract and fixtures only; no final clean result for the pilot.
- **Fixtures and negative tests:** justified shared constraint; two distinct
  clusters forced together; excluded counterexample; unresolved branch;
  incomplete inventory; multi-segment ambiguity.
- **Dependencies and level:** occurrences, observations, hypotheses, claims and
  counterevidence; mixed occurrence-, hypothesis-, claim-, and run-level.

## GENERIC_OVEREXTRACTION

- **Purpose:** ensure a proposed meaning is specific enough to explain the
  target evidence and distinguish essential neighbors.
- **Prohibited failure mode:** a broad, vague, or universally applicable label
  is presented as a discriminating Root Core or claim.
- **Mandatory inputs:** bounded hypothesis/claim, target scope, observations,
  EssentialNeighbor probes, positive and negative cases, counterevidence,
  unresolved cases, and rejection condition.
- **Acceptable evidence sources:** governed internal artifacts and admitted
  corpus evidence; derived similarity may only propose a probe.
- **Lineage:** every scope item and probe resolves to artifacts/occurrences and
  the exact hypothesis or claim revision.
- **Decision rule:** test whether the statement predicts target positives,
  excludes relevant negatives/neighbors, and is falsifiable. Flag if it survives
  only because it is generic or its scope expands after counterexamples.
- **Clean:** declared scope, discriminating neighbor tests, counterexamples, and
  executable rejection condition all pass with unresolved cases retained.
- **Failed:** non-discriminating generic label, scope drift, unfalsifiable
  wording, or ignored negative probe.
- **NOT_EVALUATED:** missing bounded statement, neighbor/negative probes,
  counterevidence, scope, or rejection condition.
- **Diagnostics:** statement/scope revision, probe set and outcomes,
  counterexamples, rejection rule, and genericity failure reason.
- **Morphology/root required:** no for evaluator logic; the evaluated artifact
  must still have governed occurrence evidence.
- **Before QAC:** yes; current pilot artifacts remain `NOT_EVALUATED` until their
  mandatory semantic inputs exist.
- **Fixtures and negative tests:** discriminating bounded claim; generic label;
  passes positives but fails neighbor; scope expansion; absent falsification;
  unresolved case retained.
- **Dependencies and level:** observations, hypotheses, claims,
  EssentialNeighbor and counterevidence; mixed hypothesis- and claim-level with
  run coverage.

## LETTER_SEMANTICS_OVERRELIANCE

- **Purpose:** prevent letter shape, sound, order, or symbolic association from
  functioning as sufficient semantic proof.
- **Prohibited failure mode:** a semantic conclusion is inferred primarily from
  individual letters or speculative letter symbolism without corpus evidence.
- **Mandatory inputs:** hypothesis/claim statement and rationale, evidence refs,
  dependency graph, corpus observations, counterevidence, and method revision.
- **Acceptable evidence sources:** governed Quran-internal observations and
  explicit linguistic evidence; letter-pattern analysis may be a bounded prompt
  for testing, never self-validating evidence.
- **Lineage:** every rationale component is typed as observation, structural,
  phonological/orthographic candidate, or external/speculative dependency.
- **Decision rule:** inspect the derivation graph. Flag when the conclusion
  depends materially on letter semantics without independent corpus support.
  Candidate use is clean only when non-letter evidence independently establishes
  the tested result and the letter pattern is not treated as authority.
- **Clean:** complete rationale/dependency classification and sufficient
  independent corpus evidence.
- **Failed:** letter-only or materially letter-dependent semantic inference,
  including a mixed rationale whose independent evidence is insufficient.
- **NOT_EVALUATED:** absent rationale, unresolved dependencies, missing evidence
  sufficiency result, or unclassified letter claim.
- **Diagnostics:** letter premise, dependency path, independent evidence refs,
  sufficiency result, affected conclusion, unresolved edges.
- **Morphology/root required:** no.
- **Before QAC:** yes.
- **Fixtures and negative tests:** independently supported result with incidental
  letter probe; letter-only claim; mixed but insufficient support; hidden letter
  premise; missing rationale/dependency.
- **Dependencies and level:** observations, hypotheses, claims, evidence and
  dependency records; mixed hypothesis- and claim-level.

## CIRCULAR_CONFIRMATION

- **Purpose:** ensure conclusions are supported by evidence independent of the
  conclusion or its derived restatements.
- **Prohibited failure mode:** a hypothesis/claim, derived card/projection, or
  mutually dependent artifact is used to confirm itself.
- **Mandatory inputs:** hypotheses/claims and revisions, evidence and
  counterevidence refs, typed derivation/dependency edges, source lineage, and
  the full reachable dependency subgraph.
- **Acceptable evidence sources:** resolvable governed records; projections and
  cards may be traced as derivatives but never count as independent support.
- **Lineage:** every support edge records origin, target, type, revision, and
  whether the target is primary evidence or derived output.
- **Decision rule:** resolve the reachable support graph, reject unresolved
  references, detect direct/transitive cycles, and remove derived restatements
  from the independent-support set. Flag a cycle or support that reduces only to
  the evaluated conclusion.
- **Clean:** graph is complete and acyclic and required support terminates in
  independent admissible evidence.
- **Failed:** direct/transitive self-support, mutual confirmation, or derived
  output treated as primary evidence.
- **NOT_EVALUATED:** unresolved references, untyped edges, incomplete reachable
  graph, or no way to determine independence.
- **Diagnostics:** cycle path or unresolved edge, derivative classification,
  independent terminal evidence, graph/revision identity.
- **Morphology/root required:** no.
- **Before QAC:** yes.
- **Fixtures and negative tests:** acyclic evidence chain; direct self-edge;
  two-node and longer cycles; card/projection feedback; missing/untyped ref;
  cross-revision stale edge.
- **Dependencies and level:** hypotheses, claims, evidence/counterevidence,
  DependencyRecord and derived projections; mixed artifact- and claim-level.

## Future structural annotation boundary

The proposed layer fits the architecture only as a new provenance-bound model;
it does not fit safely inside the current verse-level `CorpusOccurrence` row or
the two descriptive `CorpusSnapshot.structural_source*` strings.

Tanzil remains authoritative for Quran text and verse identity. A future
structural annotation record should contain:

- annotation ID and Tanzil `snapshot_id`/occurrence reference;
- `verse_ref`, word index, segment index, and multi-segment ordering;
- structural `source_id`, `source_version`, `source_hash`, artifact reference,
  and import revision;
- root, lemma, POS, form, voice, explicit features, and only permitted syntax;
- raw source locator/row identity and reconciliation status.

Required persistence constraints include a foreign key to the Tanzil-bound
occurrence/snapshot, a unique identity across snapshot + verse + word + segment
+ structural source identity, deterministic ordering, immutable source
provenance after validated import, and fail-closed handling of missing,
duplicate, ambiguous, or text-mismatched alignment. Structural annotations must
never mutate Tanzil `text`, `verse_ref`, or canonical artifact identity.

Current gaps are:

1. no token/segment structural annotation model or migration;
2. no public read/write schema carrying the structural fields and provenance;
3. no exact word/segment identity or reconciliation contract in persistence;
4. no real-format QAC parser/import service or deterministic idempotency proof;
5. current fixture import discards parsed annotations and persists only
   verse-level occurrences;
6. no field-level prohibited-content rejection at the persistence boundary;
7. no structural indexes/constraints or immutable lineage enforcement;
8. no occurrence-coverage service exposing complete root/lemma/form evidence to
   the semantic methodology and Purity evaluators.

## Ordered future dependency sequence

1. **Stage A — QAC provenance and artifact qualification:** acquire and pin the
   exact artifact; verify provenance/license; bind the expected hash candidate;
   inventory the real format and fields; define importer and structural mapping
   requirements. This stage is not admission and leaves structural role
   authorization `NOT_APPROVED`, the importer `NOT_IMPLEMENTED`, source role
   `SOURCE_ROLE_PENDING`, and production activation `NOT_AUTHORIZED`.
2. **Stage B — Structural persistence/domain support:** add the annotation model,
   migration, schemas, provenance binding, word/segment identity, indexes,
   constraints, and immutable/fail-closed rules.
3. **Stage C — Real QAC importer and validation:** parse the qualified real
   artifact, preserve segments, reject prohibited fields, reconcile to Tanzil,
   validate persistence deterministically, and provide no guessing fallback.
   This validation evidence does not admit the source or authorize production.
4. **Stage D — QAC structural-source admission decision:** only after Stages
   A-C are evidenced may governance explicitly decide `APPROVED` or
   `NOT_APPROVED`; no result is pre-authorized.
5. **Stage E — Production activation:** consider a separate activation
   transition only after an approved structural role, validated importer,
   governed artifact, persistence/reconciliation evidence, and required
   verification.
6. **Morphology-independent Purity evaluators:** implement the six dimensions
   identified above with complete evidence and negative-path tests.
7. **Morphology-dependent Purity evaluators:** complete contextual leakage and
   forced unification after structural evidence is admitted and available.
8. **Focused V1/V2 verification:** verify authority, schema, migration,
   import/reconciliation, all eight result contracts, and fail-closed gates; no
   broad release claim.
9. **Fresh independent review:** review the exact committed candidate SHA in a
   clean read-only context against this contract.
10. **Same five-root pilot rerun:** only after explicit independent acceptance for
   the intended profile. Remaining batches stay unauthorized.
