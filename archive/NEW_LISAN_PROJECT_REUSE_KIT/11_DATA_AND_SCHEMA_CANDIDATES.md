# Data and Schema Candidates

## Design rule

Extract the minimum records needed for evidence integrity and AI decision review. Do not copy Lisan3’s complete domain model, four status axes, publication workflow, Steward, gates, graph/vector persistence or governance proposal system into the first prototype. [TR-080]

## P0 records

### 1. SourceIdentity

Purpose: immutable identity and allowed use of Quran, structure and external sources.

Key fields: `source_id`, class, version/revision, artifact ref/hash, license/use status, normalization, field roles, alignment policy, known limitations.

Source basis: `CorpusSnapshot`, corpus authority, Tanzil/QAC contracts. Classification: `ADAPT`.

### 2. CorpusSnapshot

Purpose: exact Quran text/identity boundary.

Key fields: snapshot ID, source identity, canonical text hash, verse index hash/count, created/verified receipt. Avoid Lisan-specific activation lifecycle unless the new project needs it.

Classification: `ADAPT`.

### 3. Occurrence

Purpose: exact target instance.

Key fields: snapshot, verse, token/word/segment locator, source text, normalized query key, root/lemma/form annotations with source refs and ambiguity.

Current Lisan3 `CorpusOccurrence` is only verse-level; the richer boundary is specified but not implemented in the Purity contract. Classification: `ADAPT`. [TR-081]

### 4. ResearchRun

Purpose: durable container for target, protocols, sources and artifacts.

Key fields: run ID, target/analysis unit, corpus/protocol/source-profile revisions, stage, parent run, timestamps, completion vector, result refs.

Classification: `ADAPT`.

### 5. Observation

Purpose: directly verifiable structural/context record before interpretation.

Key fields: occurrence refs, typed observation fields, tool/source receipt, ambiguity, observer/model, revision.

Classification: `ADAPT`; avoid free-text fields that can hide claims. [TR-082]

### 6. EvidenceRelation

Purpose: state exactly how an item supports/challenges a hypothesis or decision.

Key fields: relation ID, source artifact/observation, target claim/hypothesis, direction (`SUPPORTS`, `CHALLENGES`, `LIMITS`, `CONTEXT_ONLY`), asserted proposition, source role, strength basis, resolver receipt.

This is missing as a first-class current Lisan3 model; opaque lists are insufficient. Classification: `ADAPT`. [TR-083]

### 7. Hypothesis

Purpose: testable candidate with branch/scope, predictions and rejection condition.

Key fields: ID/revision/parent, statement, analysis unit, lexical-unit/branch scope, predictions, evidence relations, counterevidence, unresolved cases, rejection condition, influence/source profile.

Classification: `ADAPT` from current model and legacy freeze schema.

### 8. SemanticDecision

Purpose: AI-issued preferred/competing/unresolved result.

Key fields: decision ID/revision, target/scope, disposition, preferred statement, alternatives, concise reasons, layer map, evidence/counterevidence, rejection result, result strength, completeness, verification, provenance, external influence.

New capability; classification: `ADAPT` from `SemanticClaim` without Lisan lock/publication axes. [TR-084]

### 9. ExecutionReceipt

Purpose: prove what model/Tool/Skill actually executed.

Key fields: execution ID, run/stage, actor/model/provider/config, Skill/prompt/context hashes, tool name/version, inputs/outputs refs and hashes, start/end/status/error, retry parent.

Adapt from `AIExecutionRecord`; current Lisan3 record is too coarse for per-tool proof. Classification: `ADAPT`.

### 10. CompletenessProfile

Purpose: separate research coverage from result strength.

Key fields: indexed/analyzed/validated denominators; form/construction/context/neighbor coverage; exclusions; sampling; unresolved; missing capabilities.

Adapt from the Semantic Skill coverage profile, not current scalar `QualityProfile`. Classification: `ADAPT`. [TR-085]

## P1 records

### LexicalUnitHypothesis

Identity, membership criteria, included/excluded occurrences, competing partitions, historical claim status. Missing in Lisan3. [TR-086]

### LayerAttribution

Feature, candidate layers, support/challenge relations, decision, unresolved alternatives and rejection condition.

### SemanticNeighborResult

Target/neighbor identity, shared domain, essentiality, comparison dimensions, matched cases, differences/overlaps, no-difference/unresolved disposition, implications.

Adapt from `EssentialNeighbor` and legacy distinction card.

### RejectionCondition and FalsificationRun

Keep the condition separate from its execution. Required fields: observable trigger, search space, method, confound controls, decision effect; execution receipt, cases/results and verdict. Current Lisan3 structurally validates the condition but does not prove execution. [TR-087]

### SourceAccessEvent / ExternalInfluence

Record requested source/field/stage, allow/deny outcome, content ref if disclosed, dependent artifacts and later revision effects. Adapt from `IsolationEvent` plus legacy internal-reference manifest.

### IndependentVerification

Reviewer identity/class, hidden/visible context, model/provider if any, evidence split, protocol, result, disagreements and artifact hashes. Never a bare Boolean.

## P2 records

- RetrievalCandidate and ResolutionReceipt.
- DependencyEdge for method/source/result revisions.
- EvaluationCase/Run for behavioral benchmarks.
- Derived graph/vector index manifests only after adoption triggers.

## Explicit exclusions from initial schema

- four independent Lisan status axes;
- `GateReport`/Internal Lock as semantic authority;
- ReviewDecision/publication lifecycle;
- Steward commands;
- GovernanceRule/ChangeProposal machinery;
- KnowledgeNode/KnowledgeEdge tables;
- SemanticEmbedding persistence;
- owner/release acceptance fields.

## Validation principles

1. Forbid unknown fields at trusted boundaries.
2. Use explicit enums only after terminology is approved.
3. Make source/method/result revisions immutable; create descendants for change.
4. Preserve ambiguity rather than coercing a scalar.
5. Keep observation, interpretation, evidence relation and decision separate.
6. Validate referential integrity to exact sources/occurrences.
7. Never let schema pass imply semantic validity.
8. Make absent metrics `null/not evaluated`, never optimistic defaults.
9. Keep fixtures/fake-provider data visibly non-production.
10. Store concise reasons, not private chain-of-thought. [TR-088]

## Suggested prototype boundary

Implement only SourceIdentity, CorpusSnapshot, Occurrence, ResearchRun, Observation, Hypothesis, EvidenceRelation, SemanticDecision and ExecutionReceipt in the first prototype. CompletenessProfile may initially be computed JSON. Add the rest after the first real root study exposes actual query needs. [TR-089]
