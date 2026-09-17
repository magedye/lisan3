# Gaps and Missing Capabilities

## P0 gaps

| Gap | What Lisan3 currently has | What the new project needs |
|---|---|---|
| AI-issued semantic judgment | AI proposal record; domain claim only after Lisan gate | Versioned preferred/competing/unresolved decision with evidence, reasons, alternatives and revision lineage |
| Controlled terminology | Partial Skill glossary and scattered fields; no active tracked terminology registry | Owner-approved Arabic/English glossary, forbidden synonym collisions and version migration |
| Lexical-unit identity | `LEXEME` analysis label and branch guidance, no model | First-class lexical-unit hypotheses and occurrence membership |
| Token/segment structure | Verse-level `CorpusOccurrence`; future contract only | Provenance-bound token/segment/root/lemma/form/syntax and ambiguity |
| Evidence relation | Lists of refs, DependencyRecord, conceptual resolver | First-class proposition-targeted support/challenge/limit relation |
| Exact falsification execution | Rejection-condition shape and method guidance | FalsificationRun with search receipt, inspected cases and applied consequence |
| Research completeness | Rich method checklist, two claim strings and optional scalar metrics | Computed multidimensional denominators/exclusions/sampling profile |
| Explainable result strength | Warnings and Purity scores; no calibrated strength model | Component-based strength with evidence basis and calibration program |
| Independent verification | Engineering review states and Blind Lab | Independence-class record for semantic replication/challenge |
| Pretrained-knowledge contamination | Prompt/context isolation and model exposure declarations | Honest risk model, source-blind/exposed experiments, canaries and language that avoids claiming impossible purity |
| Actual tool-use proof | Tool availability list and coarse AI record | Per-invocation authoritative receipt with inputs/outputs/errors/hashes |
| Post-analysis external comparison | Method permits it conceptually; legacy six-layer snapshot | Internal snapshot, declared external opening, influence/change record and separate support roles |

## P1 gaps

### Semantic distance and near-synonym analysis

Lisan3 has differentiation axes and a neighbor record, but no reusable multidimensional semantic-distance model. Add dimensions with evidence and an explicit no-difference/unresolved state; never collapse them into embedding similarity. [TR-118]

### Confidence calibration

No current repository artifact establishes that LOW/MODERATE/HIGH or 0–100 maps to empirical reliability. Build labeled cases, compare predicted strength to later acceptance/revision, and calibrate only after enough data. [TR-119]

### EvidenceResolver implementation

The canonical retrieval document defines it for R3, but current state says R3 not started. Implement a small candidate-to-source resolver only when discovery sources exist; do not claim Lisan3 code reuse. [TR-120]

### Simpler research workflow

Lisan3 ResearchRun persists useful state but is coupled to gate/status/publication workflows. The new project needs a smaller loop: preflight → collect → observe → hypothesize → challenge → decide → optionally compare externally → verify.

### User-facing explanation

Current semantic result fields and UI read models do not provide a tested explanation contract for “why this meaning was preferred.” Add concise reasons tied to evidence, alternatives, decisive differences, strongest counterevidence and uncertainty—not hidden chain-of-thought. [TR-121]

### Gem integration

No evidence in the repository. Required proof: stable run/result identity, citations, structured forms, Tool authorization, export, resume, branching and visible source layers. Classification: `OPEN_QUESTION`.

### Opal orchestration

No evidence in the repository. Required proof: persistent workflow state, idempotent retries, branch/join semantics, artifact passing, failure lineage and readback. Classification: `OPEN_QUESTION`.

## Gaps in current Lisan3 that should be treated as lessons, not copied

- active registries/schemas folders contain no tracked contracts;
- no first-class Interpretation, Evidence, Counterevidence, lexical-unit or semantic-branch record;
- QAC real-format import/persistence/alignment is absent;
- seven Purity dimensions have no implemented extractors/evaluators;
- current AI provider selection is environment-driven and the runtime is fake-provider-tested only;
- ToolDispatcher contains a dummy corpus search and logs only successful invocations in memory;
- AIExecutionRecord stores coarse metadata and serialized proposal output refs;
- reproduction manifest includes simulated/static claims;
- no complete semantic evaluation dataset validates root-concept quality;
- no Gem/Opal integration exists.

## Dangerous hidden gap

The phrase “Quran-internal AI induction” can overpromise when the same pretrained model may already encode dictionaries, tafsir or Islamic QA. The project can control supplied evidence and record parametric-risk, but it cannot reliably erase training knowledge through prompting. Design claims and verification language around this limitation from day one. [TR-122]
