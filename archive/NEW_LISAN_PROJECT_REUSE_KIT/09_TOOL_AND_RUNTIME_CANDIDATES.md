# Tool and Runtime Candidates

## Adoption rule

Adopt a component only when a current requirement, acceptance test and removal path exist. Lisan3’s tooling reference repeatedly shows that installed/configured/executed/passed/adopted are separate. [TR-070]

Because Gem and Opal capabilities are not evidenced in this repository, their overlap is marked **to verify**, not assumed.

| Candidate | Classification | Problem solved | Adoption trigger | Gem/Opal overlap to verify | Independent engine still required? | Main warning |
|---|---|---|---|---|---|---|
| Pydantic v2 | `REUSE_AS_IS` | Strict typed inputs/outputs; forbids undeclared fields | Any Python engine accepts AI/tool artifacts | Opal may validate workflow fields; prove strict schema/export behavior | Yes if Python owns source/evidence contracts | Schema validity is not semantic truth |
| Pydantic AI | `ADAPT` | Structured model calls, dependency injection, tools/provider abstraction | Gem/Opal cannot provide inspectable typed execution or server-side tools | Likely overlaps orchestration/model calling | Only for unenforced gaps | Avoid duplicate agent runtimes |
| Provider abstraction | `ADAPT` | Model switching, test doubles and explicit degraded mode | More than one model/provider or independent verifier | Gem/Opal may route models | A thin interface may still be needed for provenance | Silent fallback changes evidence class |
| Structured outputs | `REUSE_AS_IS` | Machine-checkable decisions/evidence references | From first prototype | May be native | Engine/schema layer needed for durable validation/readback | Do not force every thought into schema; store reviewable rationale only |
| Tool calling | `ADAPT` | Model requests deterministic operations | Any AI-run corpus search or validator | Likely native | Yes for authoritative execution receipts/source enforcement | Model claim of tool use is never sufficient |
| SQLite | `ADAPT` | Local durable runs, sources, evidence, decisions and queries | Artifact-only storage becomes hard to resume/query or enforce | Opal may persist workflow; verify export and relational constraints | Possibly; start small | Do not recreate Lisan3’s full domain model |
| SQLite indexes/FTS5 | `REUSE_AS_IS` | Exact/local Arabic text and metadata retrieval | Corpus loaded locally | Unlikely to replace exact corpus indexing | Yes unless another deterministic store proves equivalent | Define normalization/diacritic policy |
| sqlite-vec | `REFERENCE_ONLY` | Local vector candidate retrieval | A benchmark proves useful discovery and FTS is insufficient | Gem may offer semantic search | No if platform retrieval is auditable and source-separated | Lisan3 evaluation pass did not select a production model |
| Vector discovery | `ADAPT` | Neighbor/outlier/counterevidence candidate generation | Exact baseline exists and recall gap is measured | Platform may offer embeddings/retrieval | Resolver/labels still required | Similarity ≠ evidence/confidence |
| NetworkX | `REFERENCE_ONLY` | Dependency reachability, cycles, impact paths | Real graph-shaped queries become awkward in SQL | Little likely overlap | No early; simple traversal may suffice | NetworkX is not persistence or semantics |
| Graph projection | `REFERENCE_ONLY` | Rebuildable relationship view with origin/provenance | At least three downstream graph consumers or repeated traversal need | Gem may visualize; Opal may expose workflow graph | Only if source-derived projection is needed | Never create second authority store |
| Model-provider routing / LiteLLM-like layer | `OPEN_QUESTION` | Multi-provider routing/accounting/fallback | Native provider layer becomes demonstrably inadequate | Gem/Opal may already route | No separate proxy unless operationally required | Added service complexity and opaque fallback |
| Fake/test providers | `REUSE_AS_IS` | Deterministic contract/error tests | From first model integration | Platforms may offer mocks | A local fixture adapter is still useful | Fake evidence is not live semantic verification |
| Promptfoo or equivalent | `ADAPT` | Behavioral/adversarial workflow evals | Stable runnable workflow and labeled regression cases | Platform eval features may overlap | No if exportable reproducible eval exists | Lisan3 config was historically not executable; verify actual runs |
| DSPy or optimizer | `REFERENCE_ONLY` | Optimize prompts/programs against metrics | Stable trusted evaluation set and baseline | Platform prompt optimization may overlap | No | Never optimize before defining “good” |
| Hypothesis | `REFERENCE_ONLY` | Generates invariant-breaking state/data cases | Python engine has nontrivial state contracts | No material overlap | Only for Python domain logic | Does not provide semantic oracles |
| Cosmic Ray | `REFERENCE_ONLY` | Tests whether critical tests detect weakened code | Mature critical deterministic rules | No | Only if Python rule engine is safety-critical | Selective use; full-repo mutation is costly |
| Schemathesis | `REFERENCE_ONLY` | OpenAPI property/contract fuzzing | A stable HTTP API exists | Gem/Opal APIs may be managed | No if no custom API | API correctness ≠ semantic correctness |
| QAC or morphology corpus | `OPEN_QUESTION` | Root/lemma/form/segment structure | License/provenance/role/import/alignment are verified | Platform may have morphology tools | Deterministic structural adapter still needed | Current Lisan3 QAC is pending and fixture parser is not reusable runtime |
| Tanzil-style exact Quran artifact | `ADAPT` | Reproducible Quran text/verse identity | From first prototype | Platform may supply Quran text but exact version/export must be provable | Yes unless platform binds exact artifact | Copy Lisan identity principles, not its authority status |
| External RAG framework | `DO_NOT_REUSE` initially | Books/dictionaries/research retrieval | Controlled post-analysis corpus becomes large and native retrieval is insufficient | Gem may already search sources | Not initially | Keep external index separate from Quran evidence |
| LangGraph | `DO_NOT_REUSE` initially | Complex agent state graph | Opal/simple orchestrator demonstrably fails | Strong overlap with Opal | No initially | Duplicate state/orchestration layer |
| Separate graph/vector servers | `DO_NOT_REUSE` initially | Large-scale remote traversal/search | Measured scale/concurrency/performance requires them | Platform may host indexes | No initially | Infrastructure without demonstrated requirement |

## Recommended minimal runtime

1. Verified Quran text plus deterministic occurrence index.
2. Minimal structural adapter and ambiguity-preserving token/segment records.
3. Versioned JSON/Pydantic-style contracts for run, evidence, decision and execution receipt.
4. One orchestration surface (Opal if proven; otherwise a small engine).
5. One conversational surface (Gem if proven).
6. Local persistent store only when artifact directories become insufficient.
7. Fake and live provider profiles kept visibly distinct.

No vector, graph, RAG framework, optimizer, formal tool or distributed service is required to validate the core hypothesis. [TR-071]

## Capability proof for Gem/Opal

Before architecture selection, demonstrate:

- exact Tool allowlist and server-owned execution receipts;
- structured output validation with unknown-field rejection;
- stable run/artifact IDs and export;
- resume after process/session loss;
- branching and competing hypotheses;
- source-stage access controls and separate indexes;
- immutable internal snapshot then external comparison revision;
- model/provider/config provenance;
- deterministic readback and audit;
- failure/retry lineage without duplicated semantic decisions.

If any P0 property cannot be enforced or exported, a lightweight independent engine should own that boundary. [TR-072]
