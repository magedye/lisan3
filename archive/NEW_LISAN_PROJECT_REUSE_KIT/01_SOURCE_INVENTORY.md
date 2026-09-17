# Source Inventory

## Reading key

`C` = canonical; `AD` = active derived; `I` = implementation evidence; `T` = test evidence; `S` = state/durable evidence; `H` = historical/reference. A source can appear in several categories because it answers different questions.

| # | Source area | High-value sources reviewed | Evidence class | Material contribution |
|---:|---|---|---|---|
| 1 | Policy and authority | `AGENTS.md`; `backend/AGENTS.md`; `AUTHORITY_MAP.md`; `PROMPT/1.MD` | C | Source precedence, claim/evidence discipline, AI and corpus boundaries, separation of implementation/review/acceptance. |
| 2 | Methodology | `skills/lisan-semantic-extraction/SKILL.md` §§0–30; `main skills/SKILL_LISAN_QURANIC_SEMANTIC_EXTRACTION_REVISED.md` | AD, H | Target contract, corpus-first induction, workflow, coverage, branching, differentiation, falsification, result shape. |
| 3 | Terminology | Semantic Skill §§2–5, 21–22; domain enums/models; legacy root/distinction schemas | AD, I, H | Operational distinctions among Root Core, Definition, Meaning, Concept, Local Meaning, Observation, Hypothesis, Claim, and status. |
| 4 | Quran/corpus | `ADMISSION_TANZIL.md`; `ADMISSION_QAC.md`; `CorpusSnapshot`; `CorpusOccurrence`; corpus authority/import services | C, I | Source identity, byte/hash binding, text/identity authority, auxiliary-structure separation, fail-closed admission. |
| 5 | Morphology/structure | Purity contract §§Contextual Leakage, Forced Unification, Future structural annotation; QAC/Tanzil adapters; alignment service | C, I | Needed token/segment identity, root/lemma/form/syntax provenance, multi-segment preservation, current implementation gaps. |
| 6 | Semantic runtime | Semantic Skill workflow; `ResearchRun`, `ObservationArtifact`, `Hypothesis`, `EssentialNeighbor`, `SemanticClaim`; Slice B/C endpoints | AD, I | Persisted research stages and semantic artifacts; current path from run to observation/hypothesis/differentiation/claim. |
| 7 | Evidence | Platform provenance model; hypothesis/claim fields; `DependencyRecord`; `EvidenceResolver` contract | C, I | Claim-to-source traceability and candidate-to-resolved-artifact boundary; current model has references but no first-class Evidence table. |
| 8 | Counterevidence | Semantic Skill §§8–10, 22; Hypothesis/Neighbor/Claim fields; legacy cards | AD, I, H | Counterexample search, strongest counterevidence, unresolved cases, failed predictions, neighbor challenge. |
| 9 | Falsification | Semantic Skill §§8–10; Pydantic `RejectionCondition`; `test_slice_c.py` | AD, I, T | Operational rejection condition, circular-condition rejection, bounded search and decision effect. |
| 10 | Root concept | Semantic Skill §§4, 7–12, 21–22, 28–30; legacy root-card and semantic-family schemas | AD, H | Minimal positive invariant, layer separation, lexical branching, hard cases, distinctive residue, non-forced outcomes. |
| 11 | Local meaning | Semantic Skill `TARGET_CONTRACT`, P2, §11, quick-answer profile | AD | Local meaning as a layered realization; narrower answer must not masquerade as a root-core result. |
| 12 | Semantic neighbors/differentiation | Semantic Skill §§5–9; `EssentialNeighbor`; legacy distinction-card schemas | AD, I, H | Essential neighbor selection, shared domain, positive difference, substitution as probe, boundary/negative cases. |
| 13 | Source-role controls | Corpus admission contracts; Blind Lab; QAC semantic quarantine; Purity Heritage/Tafsir/Dictionary dimensions | C, I, T | Explicit allowed/prohibited role, field-level quarantine, chronology/access logging, separation of blocked read from contamination. |
| 14 | Retrieval | Hybrid Retrieval §§1–35; vector contracts/service; graph service | C, I | Exact retrieval, vector/graph discovery, typed candidates, separate spaces, rebuildable derived state, deterministic resolution boundary. |
| 15 | AI runtime | Platform AI section; tooling §5; `ai_provider.py`; `ai_context.py`; `ai_tools.py`; AI endpoint and tests | C, I, T | Structured output, provider abstraction, context injection, actual tool inventory, execution record, fake/live distinction; current runtime remains thin. |
| 16 | Skills | Active semantic Skill; repository execution/verification/hybrid Skills | AD | Fixed protocol structure, preflight, required outputs, failure modes, verification cadence. |
| 17 | Agent patterns | `LISAN3_HANDOFF.md` §§19–21; semantic workflow; Blind Lab/falsification separation | S, AD | Orchestration lessons, independent-review boundary, when role separation adds value and when it is ceremony. |
| 18 | Tools | Tooling reference §§3–18; dependency files; vector runtime reports | C, I, S | Pydantic, Pydantic AI, SQLite, FTS, NetworkX, sqlite-vec, testing/eval tools, adoption triggers and deliberate non-adoptions. |
| 19 | Schemas/contracts | `backend/domain/models.py`; `schemas.py`; `vector_contracts.py`; OpenAPI; legacy JSON schemas | I, H | Candidate data structures, strict-extra schemas, immutable provenance, branch/distinction/freeze templates; no active JSON schema registry. |
| 20 | Confidence/status concepts | Four status axes; `QualityProfile`; Purity contract; semantic Skill §§5–6; legacy `confidence` fields | C, I, H | Strong warning against one overloaded score; current implementation mixes some computed, persisted, and unavailable metrics. |
| 21 | Blind Lab/independent verification | Isolation service/context builder; Slice B and AI tests; graph/vector access controls; legacy optional rediscovery audit | I, T, H | Content isolation beyond UI, auditable denied access, actual exposure distinction, limits of same-model independence. |
| 22 | Tests/evaluations | `test_slice_b/c/c_ai`; `test_purity`; `test_properties`; corpus/methodology tests; R1/R2 suites; legacy regressions | T, H | Negative-path patterns, property/mutation testing, deterministic fixtures, explicit non-authority, known missing semantic eval depth. |
| 23 | Reproducibility/provenance | Methodology source hash; corpus snapshot hashes; AI execution records; reproduction manifests; vector manifest/config hash | C, I, S | Immutable source identity, exact inputs/revisions, replay limits, derived-index invalidation; runtime manifest has known simulated/static fields. |
| 24 | UX/research interaction | Run workspace and Attention read models; Ask fallback; Knowledge Explorer authority notice; UX checkpoints | I, S | Research workspace aggregation, visible uncertainty, provenance access, unavailable-result behavior; detailed visual UI is outside reuse scope. |
| 25 | Tooling decisions | `LISAN_TOOLING_ADOPTION_REFERENCE.md`; R2 benchmark/infrastructure reports | C, S | Requirement/trigger-based adoption, benchmark-before-optimization, local-first progression, duplicate-workflow avoidance. |
| 26 | Lessons/historical material | `PROJECT_STATE.md`; `LISAN3_HANDOFF.md`; semantic-pilot reports; QAC Stage-A; `LISAN_LEGACY_REUSE_DELTA_KIT_v1.0/` | S, H | Actual failure classes: migration drift hidden by tests, cosmetic Purity, verse-only structure, admission-order contradiction, benchmark false positives, legacy freeze/firewall ideas. |

## Required-source coverage notes

- Current policy and every canonical document named by the owner were reviewed.
- Corpus/source admission and Purity/structural evidence contracts were read directly.
- Active backend models, schemas, AI context/provider/tools, run admission, isolation, gates, Purity, graph/vector, corpus authority/adapters, and methodology binding were inspected.
- Evidence/Counterevidence are represented mostly as fields and references; no current first-class `Evidence` or `Counterevidence` persistence class exists.
- Blind Lab and ResearchRun were checked in code and negative tests.
- Existing reuse material was treated as historical; its own manifest still labels most items `CANDIDATE_FOR_ADOPTION` with compatibility evidence `TBD`.
- Generated OpenAPI was recognized as a contract artifact but not deeply reread field-by-field because the Python contracts are the higher-value semantic source.
- Generated UI assets, dependencies, databases, screenshots, caches, and build outputs were excluded from deep review.

## Material absences discovered

1. Active `registries/` and `schemas/` contain no tracked files at the reviewed HEAD.
2. No first-class current Evidence, Counterevidence, lexical-unit, semantic-branch, source-access, or research-completeness model exists.
3. Current `CorpusOccurrence` is verse-level and lacks token/segment/morphology fields.
4. QAC adapter/alignment code is explicitly fixture-grade and not a real-format admitted pipeline.
5. Seven of eight current Purity evaluator dimensions always return `NOT_EVALUATED`; even Dictionary-First uses only a timestamp heuristic.
6. Current AI tooling registers a dummy corpus search and records tool availability, but not a complete per-invocation input/output/error trace in `AIExecutionRecord`.
7. No Gem or Opal integration evidence exists in the repository.
8. Current AI proposal path stores serialized proposal output as an artifact reference but does not itself create the domain Hypothesis; this is a useful separation, though the new project may intentionally give AI a controlled decision command.

## Second-pass missed-material search

The second pass searched for `root`, `lexeme`, `local meaning`, `evidence`, `counterevidence`, `rejection`, `contamination`, `neighbor`, `confidence`, `coverage`, `AIExecutionRecord`, `ResearchRun`, `RetrievalCandidate`, and historical regression/schema artifacts. It added the legacy initial-hypothesis freeze, internal-reference manifest, semantic-family maps, critique/revision record, QAC gloss firewall, sparse-evidence ceiling, supporting-semantics firewall, R2 false-positive benchmark, and five-root blocker evidence to the initial canonical/code inventory.
