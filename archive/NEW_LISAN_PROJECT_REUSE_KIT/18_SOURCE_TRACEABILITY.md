# Source Traceability

## How to read this ledger

Every substantive extraction or recommendation in this kit carries a `[TR-nnn]` tag. Each row below covers every tag in its stated interval and identifies the repository evidence that supports the observation, plus the inference boundary where this kit recommends a different new-project design. A range does not imply that every source proves every sentence: the `Inference boundary` column states what was added by this review.

Evidence classes are: `CANONICAL`, `ACTIVE_DERIVED`, `IMPLEMENTATION`, `TEST`, `STATE_REPORT`, `HISTORICAL`, `OWNER_DIRECTION`, and `AGENT_INFERENCE`. Historical material is never treated as current Lisan3 authority. `PROJECT_STATE.md` and evidence reports describe reviewed state; they do not override code or canonical contracts.

## Terminology and root method

| Trace tags | Repository source and locator | Class | Tests or executable evidence | Inference boundary |
|---|---|---|---|---|
| TR-001 | `skills/lisan-semantic-extraction/SKILL.md` §§2–5, 21–22; `backend/domain/models.py` status/result models; `LISAN_LEGACY_REUSE_DELTA_KIT_v1.0/schemas/*.json` | ACTIVE_DERIVED, IMPLEMENTATION, HISTORICAL | Schema/model validation tests throughout `tests/test_slice_*.py` | Candidate Arabic labels and the recommendation for an owner-approved terminology charter are AGENT_INFERENCE. |
| TR-002–TR-012 | Semantic Skill target contract, principles P2/P3 and coverage; current models; legacy occurrence, distinction, freeze and result schemas | ACTIVE_DERIVED, IMPLEMENTATION, HISTORICAL | `tests/test_slice_b.py`, `tests/test_slice_c.py`, legacy regression cases | The nine missing terms, forbidden synonym-collision mechanism and ordering before schema/prompt work are AGENT_INFERENCE. |
| TR-013–TR-016 | Semantic Skill §§2–6, 9, 12, 21; `docs/evidence/semantic-pilot-2026-08-26/SEMANTIC_PILOT_BLOCKER_REPORT.md` | ACTIVE_DERIVED, STATE_REPORT | Pilot manifest/results and acceptance matrix | Requiring an explicit lexical-unit set and proposed sampling use are adaptations for the independent project. |
| TR-017–TR-021 | Semantic Skill §7 and Phases 2–6, especially layer attribution, hard cases, competing hypotheses and differentiation axes; legacy initial-hypothesis freeze | ACTIVE_DERIVED, HISTORICAL | `tests/test_slice_c.py`; legacy stress/freeze regressions | The participant-role inventory and “freeze serious hypotheses” workflow are concise AGENT_INFERENCE adaptations. |
| TR-022 | Semantic pilot blocker report and corrective addendum; `backend/domain/models.py::CorpusOccurrence` | STATE_REPORT, IMPLEMENTATION | Five pilot result YAML files and acceptance matrix | The new-project consequence is AGENT_INFERENCE. |
| TR-023 | Semantic Skill §10; `backend/domain/schemas.py::RejectionCondition` | ACTIVE_DERIVED, IMPLEMENTATION | `tests/test_slice_c.py` circular-rejection cases | Requiring an attached execution receipt goes beyond the current schema and is AGENT_INFERENCE. |
| TR-024–TR-026 | Semantic Skill §§6, 10, 12.1, 20–22; `backend/domain/models.py::QualityProfile` | ACTIVE_DERIVED, IMPLEMENTATION | Slice C and Purity tests; pilot evidence | The proposed strength-component direction is AGENT_INFERENCE; no weights or calibration claim is inherited. |
| TR-027–TR-028 | Owner-supplied new-project context, contrasted with Semantic Skill P3 and current AI proposal boundary | OWNER_DIRECTION, ACTIVE_DERIVED | `tests/test_ai_runtime.py`; current AI endpoint/service behavior | AI-issued preferred decisions and the suggested one-root experiment are AGENT_INFERENCE, not Lisan3 authority. |

## Layering, evidence and source control

| Trace tags | Repository source and locator | Class | Tests or executable evidence | Inference boundary |
|---|---|---|---|---|
| TR-029–TR-030 | Semantic Skill P2 and §11 | ACTIVE_DERIVED | Semantic-pilot evidence exposes the consequence of absent structural layers | Treating the equation as a non-additive attribution checklist is this review’s clarification. |
| TR-031 | Semantic-pilot blocker report/corrective addendum; five root result YAML files; current occurrence model | STATE_REPORT, IMPLEMENTATION | Pilot artifacts preserve null Root Core and blockers | “Prevented fabricated structural evidence” is an evidence-backed interpretation. |
| TR-032 | `docs/canonical/ADMISSION_QAC.md`; `backend/domain/services/corpus/qac.py` | CANONICAL, IMPLEMENTATION | `tests/test_corpus_adapter.py::test_qac_adapter_semantic_quarantine` | Generalizing field-role quarantine beyond QAC is AGENT_INFERENCE. |
| TR-033 | `backend/domain/schemas.py::ObservationArtifactCreate` | IMPLEMENTATION | `tests/test_slice_b.py` observation rejection | The free-text residual risk is AGENT_INFERENCE from the allowed schema. |
| TR-034–TR-037 | Semantic Skill §§7–13 and anti-patterns; platform governance boundary | ACTIVE_DERIVED, CANONICAL | Slice C structural tests; pilot blocker evidence | Simplifying governance coupling and the proposed layer-attribution record are AGENT_INFERENCE. |
| TR-038–TR-040 | Platform corpus/provenance sections; `ADMISSION_TANZIL.md`; `ADMISSION_QAC.md`; Purity contract | CANONICAL | Corpus authority/import/activation and QAC quarantine tests | The independent-project source-role profile is AGENT_INFERENCE. |
| TR-041 | Hybrid Retrieval §§22–25, 35 | CANONICAL | `PROJECT_STATE.md` records R3 not started | Reusing the boundary without claiming implementation is the recommendation. |
| TR-042–TR-043 | Hybrid Retrieval §25; `backend/domain/services/isolation.py`; AI context and graph/vector access mediation | CANONICAL, IMPLEMENTATION | `tests/test_slice_b.py` contamination/audit cases; graph/vector isolation tests | New-project access-outcome vocabulary is AGENT_INFERENCE. |
| TR-044 | Platform methodology revision contract; `backend/domain/services/methodology_authority.py`; migration `e8b3f6a1c204_*` | CANONICAL, IMPLEMENTATION | `tests/test_methodology_authority.py` | Binding a lighter result to protocol/source profiles is AGENT_INFERENCE. |
| TR-045 | Semantic Skill tool-reality rules; `backend/domain/services/ai_tools.py` | ACTIVE_DERIVED, IMPLEMENTATION | `tests/test_ai_runtime.py` | Adding failed-call and exact-output receipts is AGENT_INFERENCE based on implementation gaps. |
| TR-046–TR-049 | Tanzil/QAC admission, Purity contract, Blind Lab and legacy internal-reference/freeze/six-layer schemas | CANONICAL, IMPLEMENTATION, HISTORICAL | Corpus, isolation and legacy regression tests | The minimum evidence record, contamination probes and staged comparison flow are AGENT_INFERENCE. |

## Skills, agents and tools

| Trace tags | Repository source and locator | Class | Tests or executable evidence | Inference boundary |
|---|---|---|---|---|
| TR-050–TR-063 | `skills/lisan-semantic-extraction/SKILL.md` target contract, Phases 1–9, §§6–13 and 20–30; corpus contracts; Purity contract | ACTIVE_DERIVED, CANONICAL | Relevant corpus, Slice B/C, Purity and AI runtime tests | The 13 separate Skill specifications, interfaces and adoption cautions are AGENT_INFERENCE candidates. |
| TR-064–TR-066 | Semantic workflow; Blind Lab; `LISAN3_HANDOFF.md` independent-review and agent-execution lessons | ACTIVE_DERIVED, IMPLEMENTATION, STATE_REPORT | Isolation and AI tests | Proposed Agent partition and independence taxonomy are AGENT_INFERENCE. |
| TR-067 | Platform persisted-state/gate policy; `backend/domain/services/gates.py`; `run_admission.py` | CANONICAL, IMPLEMENTATION | `tests/test_properties.py`, `tests/test_gates_mutation.py`, run-admission tests | Applying server-owned state to a lighter orchestrator is AGENT_INFERENCE. |
| TR-068–TR-069 | Current AIExecutionRecord/provider/tool/context implementation; owner Gem/Opal proposal | IMPLEMENTATION, OWNER_DIRECTION | `tests/test_ai_runtime.py` | Capability questions and prohibition on Boolean independence are AGENT_INFERENCE. |
| TR-070–TR-072 | `docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md` §§3–18; platform runtime sections; current dependencies/services | CANONICAL, IMPLEMENTATION | Tool-specific suites and durable R1/R2 reports | The adoption order, Gem/Opal comparison and independent-engine trigger are AGENT_INFERENCE. |

## Retrieval, data and evaluation

| Trace tags | Repository source and locator | Class | Tests or executable evidence | Inference boundary |
|---|---|---|---|---|
| TR-073–TR-075 | Hybrid Retrieval §§7–12, 22–25; `backend/domain/vector_contracts.py::RetrievalCandidate` | CANONICAL, IMPLEMENTATION | `tests/test_r2_vector_contracts.py`, vector API tests | New-project candidate uses and minimum metadata are adaptations. |
| TR-076 | `tools/governance-lab/reports/R2_VECTOR_BENCHMARK_DECISION.md`; benchmark results/cases | STATE_REPORT | `tools/governance-lab/vector-benchmark/r2/test_benchmark_contract.py` | Treating the failure as a warning against aggregate-score adoption is evidence-backed inference. |
| TR-077–TR-079 | Hybrid Retrieval §§15–24; `backend/domain/services/knowledge_graph.py` | CANONICAL, IMPLEMENTATION | `tests/test_r1_knowledge_graph.py`; R1 reports/state | Exact-first prototype order and graph deferral are AGENT_INFERENCE. |
| TR-080–TR-082 | `backend/domain/models.py` and `schemas.py`: CorpusSnapshot, CorpusOccurrence, ResearchRun, ObservationArtifact, Hypothesis, SemanticClaim | IMPLEMENTATION | Slice B/C, corpus and schema tests | The minimum model subset and richer occurrence/evidence shapes are AGENT_INFERENCE. |
| TR-083–TR-089 | Same models plus AIExecutionRecord, EssentialNeighbor, QualityProfile; Semantic Skill coverage; legacy branch/freeze/test records | IMPLEMENTATION, ACTIVE_DERIVED, HISTORICAL | AI, Slice C and legacy regressions | First-class EvidenceRelation, SemanticDecision, CompletenessProfile, LexicalUnitSet and receipt shapes are AGENT_INFERENCE. |
| TR-090–TR-094 | Semantic Skill coverage/falsification; Purity contract; Blind Lab implementation; `RejectionCondition` | ACTIVE_DERIVED, CANONICAL, IMPLEMENTATION | Purity, isolation and Slice C tests | Three-axis assessment and measurable component list are AGENT_INFERENCE; weights remain intentionally unset. |
| TR-095–TR-098 | Purity contract eight dimensions and `backend/domain/services/purity.py` | CANONICAL, IMPLEMENTATION | `tests/test_purity.py`; current state/pilot show evaluator gaps | Decoupling diagnostics from one monolithic gate is AGENT_INFERENCE for the more autonomous project. |
| TR-099 | Test inventory and durable reports; `PROJECT_STATE.md` | TEST, STATE_REPORT | Tests were inspected, not rerun for this documentation-only review | The conclusion that no current end-to-end semantic truth benchmark exists follows from the reviewed suite. |
| TR-100–TR-103 | `LISAN_LEGACY_REUSE_DELTA_KIT_v1.0/REUSE_MANIFEST.json`, regression cases and `test-record.schema.json`; current tooling reference | HISTORICAL, CANONICAL | Historical cases plus current property/mutation/contract suites | Proposed evaluation-case structure and staged adoption are AGENT_INFERENCE. |

## Retrospective, gaps and recommendations

| Trace tags | Repository source and locator | Class | Tests or executable evidence | Inference boundary |
|---|---|---|---|---|
| TR-104 | Tanzil/QAC contracts and services; run admission; isolation; gates; graph/vector; pilot reports | CANONICAL, IMPLEMENTATION, STATE_REPORT | Corpus, Slice B, gate/property/mutation, R1/R2 tests | Identifying these as controls that prevented error is evidence-backed synthesis. |
| TR-105 | `LISAN3_HANDOFF.md` V3 findings and later closure notes | STATE_REPORT | Named migration, OpenAPI, mutation, Schemathesis, browser and Hypothesis evidence in handoff | Lessons for rebuilding are AGENT_INFERENCE. |
| TR-106–TR-108 | Platform governance/data contracts; current models/migrations; pilot evidence; legacy schemas | CANONICAL, IMPLEMENTATION, STATE_REPORT, HISTORICAL | Relevant migration/status/corpus tests | Complexity-value assessment and “build earlier” ordering are AGENT_INFERENCE. |
| TR-109 | Tooling reference deferrals; R2 decision report | CANONICAL, STATE_REPORT | R2 benchmark artifacts | New-project postponement is AGENT_INFERENCE. |
| TR-110–TR-112 | Semantic Skill AI roles/anti-patterns; current AI runtime; Purity/Blind Lab; five-root pilot | ACTIVE_DERIVED, IMPLEMENTATION, STATE_REPORT | AI, Purity, isolation tests and pilot acceptance matrix | Autonomy/governance balance is AGENT_INFERENCE. |
| TR-113 | Hybrid R3 contract/state; current result fields; reproduction manifest; empty tracked `registries/`/`schemas/`; QAC alignment service | CANONICAL, IMPLEMENTATION, STATE_REPORT | Existing service/tests demonstrate current boundaries | “Elegant but limited practical value” is a scoped retrospective judgment. |
| TR-114–TR-116 | Cross-cutting contracts, strict schemas, migrations, source services, graph/vector and test reports | CANONICAL, IMPLEMENTATION, TEST, STATE_REPORT | Named suites and reports | Robust-pattern selection and concluding synthesis are AGENT_INFERENCE. |
| TR-117 | Reuse matrix C37–C49; legacy authority/status/card schemas; tooling deferrals | CANONICAL, HISTORICAL, AGENT_INFERENCE | Pilot and benchmark evidence show some present costs | Anti-reuse is explicitly a recommendation; later triggers can reopen it. |
| TR-118–TR-122 | Semantic Skill differentiation; current models/UI read models; hybrid R3 state; owner Gem/Opal context; model-isolation limits | ACTIVE_DERIVED, IMPLEMENTATION, STATE_REPORT, OWNER_DIRECTION | R2/pilot evidence and current absence checks | Proposed distance model, calibration, explanation, integration questions and claim-language limits are AGENT_INFERENCE. |
| TR-123–TR-127 | Reuse matrix C01–C50 and all source areas above | CANONICAL, ACTIVE_DERIVED, IMPLEMENTATION, TEST, STATE_REPORT, HISTORICAL, AGENT_INFERENCE | Cross-referenced suites/reports above | Recommended foundations/adaptations/experiments/deferrals/risks are AGENT_INFERENCE, not final architecture. |
| TR-128–TR-130 | Owner goal plus evidence that current pilot lacked structural/evaluator readiness | OWNER_DIRECTION, STATE_REPORT | Semantic-pilot artifacts | Suggested prototype and success criteria are AGENT_INFERENCE requiring owner decision. |

## Classification traceability

Candidate-level sources, locators, dependencies, risks and omission/import consequences are recorded in `02_REUSE_MATRIX.md` as C01–C50. The matrix assigns exactly one primary classification to each candidate. This trace ledger supports the prose recommendations; it does not supersede the matrix.

## Known evidence limits

- Tests were inspected for contract intent and historical evidence; they were not rerun because this task changes no runtime code.
- No repository evidence establishes calibrated numeric semantic confidence or genuine absence of relevant pretrained-model knowledge.
- Canonical EvidenceResolver design is not implementation evidence.
- Historical reuse schemas remain candidate/reference material unless independently selected for the new project.
- Gem and Opal capabilities are owner-proposed and unverified in this repository.
