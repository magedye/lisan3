# Semantic Layering Kit

## Core decomposition

Lisan3’s most reusable semantic error-control is the analytic equation:

```text
LOCAL MEANING
= ROOT OR LEXICAL-UNIT CONTRIBUTION
+ MORPHOLOGICAL FORM / DERIVATION
+ CONSTRUCTION / SYNTAX
+ PARTICIPANT ROLES
+ DISCOURSE / CONTEXT
```

It is a decomposition checklist, not a claim that every term contributes independently or additively in every occurrence. Source: active Semantic Skill P2. [TR-029]

## Layer contract candidates

| Layer | Question | Minimum evidence | Common attribution error | Candidate output |
|---|---|---|---|---|
| Root contribution | What persists across relevant lexical units/derivations, if anything? | Cross-family distribution with competing branch test | Assuming the written root guarantees one semantic invariant | `root_contribution_candidate` or unresolved |
| Lexical-unit contribution | What is stable for this usage-bearing unit? | Occurrence cluster, derivational and construction distribution | Pooling another lexical unit’s evidence | `lexical_unit_meaning` with identity/scope |
| Morphological form | What contrast follows the form/pattern? | Controlled form comparisons and counterexamples | Projecting a form’s effect into root core | `form_effect_candidate` with status |
| Derivation | What changes with derivational family? | Cross-derivative comparison under similar constructions | Treating etymological relation as semantic identity | `derivational_relation` |
| Construction | What comes from valency, preposition, complement or fixed frame? | Same lexeme across constructions and neighbor contrasts | Calling a constructional effect lexical meaning | `construction_effect` |
| Syntax | What relation is structurally present? | Provenance-bound parser/manual annotation | Treating a parse as semantic truth | `structural_observation` |
| Participant roles | Which participant configuration shapes the event? | Role-linked occurrences and contrasts | Importing agent/patient properties into root | `participant_frame` |
| Discourse | What comes from reference, contrast, information structure or surrounding discourse? | Declared span and dependency | Expanding immediate word meaning to passage theme | `discourse_effect` |
| Context | What local/pragmatic realization is licensed here? | Exact context window and comparison | Treating contextual outcome as invariant | `context_effect` |
| Local meaning | What does this expression mean at this specific location after layer interaction? | All applicable layer assignments plus unresolved residue | Reporting it as the root meaning | `local_meaning_decision` |
| Broader concept | What cross-text conceptual network is being analyzed? | Explicit included lexemes/relations and scope | Treating conceptual association as lexical evidence | `concept_model` |

## Attribution workflow

1. Record structural facts without semantic labels.
2. Generate candidate contribution assignments per layer.
3. For every feature, test the nearest alternative layer.
4. Compare controlled occurrence pairs when possible.
5. Record unresolved assignment rather than forcing ownership.
6. Build local meaning from the supported interaction.
7. Only then test whether any minimal feature survives as root contribution.

This reverses a common failure pattern: begin with an intuitive root definition, then push every observed effect into it. [TR-030]

## Where layering prevented real classes of error

### Semantic-pilot refusal

Lisan3’s five-root pilot did not infer root/form/construction facts from verse text, orthography or model memory because the production snapshot lacked token/segment/root annotations. Root Core remained null. That is concrete evidence that layer/evidence controls prevented fabricated structural evidence. Source: semantic-pilot blocker report and corrective addendum. [TR-031]

### QAC field quarantine

The QAC candidate is restricted to a possible structural role; glosses, translations, ontology/semantic labels and derived conclusions are excluded. `test_qac_adapter_semantic_quarantine` demonstrates the intended firewall on fixture input. This prevents a structural layer from smuggling a semantic conclusion. Source: `ADMISSION_QAC.md`, QAC adapter/test. [TR-032]

### Observation schema boundary

`ObservationArtifactCreate` forbids extra fields and `test_observation_rejection` rejects `semantic_definition`. This prevents an interpretation from entering a structural record merely through a convenient JSON field. It does not prevent semantic wording inside allowed free-text fields, so it is partial. [TR-033]

### Neighbor and root-form controls

The active Skill’s specific anti-patterns and tests expose generic roots, form projection, context leakage, structural overpromotion and invented neighbor distinctions. These are method-level protections; current tests do not establish semantic correctness on real roots. [TR-034]

## Where layering becomes unnecessarily restrictive or complex

1. Lisan3 often couples layer correctness to full governance/lock/publication state. The new project can keep layer attribution while allowing AI to issue a bounded judgment. [TR-035]
2. Definition, Meaning, Concept and Abstract Root Core risk becoming four restatements unless each has a distinct consumer and non-overlapping contract.
3. A mandatory six-layer result for every small local-meaning question creates empty ceremony. Choose the smallest applicable layers.
4. Requiring an admitted production structural source before any exploratory morphology can block learning. The new project may use clearly labeled provisional structural analyses, provided they never masquerade as verified evidence.
5. A fully persisted graph of every layer relationship should wait until real queries justify it.

## Deterministic versus model responsibilities

Deterministic Tools should own:

- Quran snapshot and exact text lookup;
- token/segment identifiers and source-bound annotations;
- occurrence collection under declared matching rules;
- morphology/syntax adapter output and ambiguity preservation;
- coverage counts and exclusions;
- source access receipts;
- evidence/reference resolution;
- dependency/cycle checks.

AI should own:

- proposing lexical units and clusters;
- judging plausible contribution assignments;
- generating and ranking hypotheses;
- identifying semantic neighbors and difference dimensions;
- explaining a preferred local/root interpretation;
- revising a conclusion after counterevidence;
- explicitly declaring uncertainty.

AI judgments remain reviewable because their factual inputs and transformations are recorded. [TR-036]

## Negative tests for each layer

- **Root vs form:** a feature appears only in one form; root claim must weaken or move.
- **Root vs construction:** change preposition/valency while root stays; claimed invariant must survive or narrow.
- **Lexical unit vs branch:** evidence from LU1 must not satisfy LU2 completeness.
- **Participants:** change affected entity/agency; participant-specific effect must not become root contribution.
- **Context:** an apparently essential feature disappears in another context.
- **Local vs broad concept:** conceptual association must not support a local lexical claim without occurrence evidence.
- **Form difference:** two different forms show no supported semantic distinction; system must return no distinction established.
- **Ambiguous assignment:** at least two layers remain plausible; system must preserve ambiguity and reduce strength.

## Candidate layer-attribution record

```yaml
feature_id: "F..."
description: "observable or inferred feature"
source_occurrences: ["occ:..."]
candidate_layers:
  - layer: "LEXICAL_UNIT"
    support: ["evidence:..."]
    challenges: ["counterevidence:..."]
  - layer: "CONSTRUCTION"
    support: ["evidence:..."]
decision: "LEXICAL_UNIT | FORM | CONSTRUCTION | PARTICIPANT | DISCOURSE | CONTEXT | UNRESOLVED"
reasons: ["concise reviewable reason"]
confidence_basis: ["test:..."]
rejection_condition: "..."
```

This is an agent recommendation, not a copied Lisan3 schema. [TR-037]
