# LISAN-Quran-Embedding and Quranic Lisan Implementation Plan

> **For Hermes:** Execute only after a separately authorized work package. Keep `LISAN-Quran-Embedding` and `lisanapp3` independent; do not train, adopt a model, or modify LISAN3 from the research repository.

**Goal:** Provide a local, reproducible, six-space candidate-discovery capability that helps Quranic Lisan research find material for inspection while never treating embedding similarity as Quranic semantic evidence, tafsir, a claim verdict, or Gate authority.

**Architecture:** `LISAN-Quran-Embedding` remains an independent research/evaluation and provenance-governance repository. `lisanapp3` owns the governed runtime, SQLite-derived indexes, candidate ledger, EvidenceResolver, Blind-Lab source policy, and user-visible retrieval workflows. Integration is through immutable, versioned handoff artifacts only—not a Python import, mutable repository path, virtual environment, model-cache, or shared runtime database.

**Tech stack:** Python 3.12, Pydantic v2, PyYAML, NumPy, pytest, Ruff in LQE; existing Lisanapp FastAPI, SQLAlchemy/Alembic, SQLite, Pydantic v2, Next.js/TypeScript; `sqlite-vec` only after the R2 spike and explicit adoption gate pass.

---

## 1. Recommended operating boundary

### Purpose

LQE may produce only reproducible, provenance-bound research artifacts:

- candidate-neighbor retrieval evaluation;
- six-space benchmark metrics and adversarial failure analysis;
- governed training-data candidates and independent-review records;
- model/tokenizer provenance matrices;
- immutable candidate handoff manifests.

Lisanapp may consume a qualified handoff only to display and route **retrieval candidates** for human/governed research inspection.

### Non-negotiable authority boundary

```text
Embedding similarity != Quranic semantic evidence
Retrieval score != epistemic confidence
Model output != Quranic semantic truth
Retrieval candidate != canonical Evidence
Candidate retrieval != Gate PASS / Internal Lock / publication authority
```

Neither repository may:

- infer Quranic meaning, Root Core, Distinctive Residue, or claim truth from a vector score;
- automatically accept a neighbor, counterevidence item, or graph relation;
- let retrieval output create canonical Evidence, a Gate outcome, or a status transition;
- use an index, cache, tokenizer, model, or prompt context to bypass Blind-Lab source restrictions;
- compare, pool, or rank vectors across incompatible embedding spaces.

## 2. Target design

### 2.1 Two-repository, immutable-handoff architecture

```text
CANON-001 admitted Quran corpus
        |
        +--> LISAN-Quran-Embedding (independent research)
        |       - benchmark and dataset governance
        |       - provenance survey
        |       - pinned-model evaluation, only when authorized
        |       - signed/hash-bound candidate handoff artifact
        |
        +--> lisanapp3 (governed product)
                - exact retrieval (primary source resolution)
                - derived vector index per approved space
                - RetrievalCandidate ledger
                - EvidenceResolver
                - Blind-Lab isolation
                - research UI and audit trail
```

**Handoff rule:** Lisanapp receives a versioned JSON/YAML artifact with hashes and explicit capability restrictions. It must not import LQE modules, reference `D:\APP\tafseer\LISAN-Quran-Embedding`, consume mutable experiment output, or share the LQE virtual environment.

### 2.2 Retrieval layers in Lisanapp

1. **Exact Retrieval — authoritative source lookup**
   - Quran reference, exact text, root/lemma/form/structural records only where their source is admitted.
   - Resolves source identity; it remains primary when it conflicts with derived retrieval.

2. **Vector Discovery — derived candidate discovery**
   - Produces candidate neighbors, distinctions, counterevidence leads, and bounded external-research leads.
   - Uses an independently selected, provenance-qualified model only.
   - Never resolves a semantic question.

3. **Graph Projection — derived governed-record navigation**
   - Projects existing governed dependencies/relationships into SQLite.
   - Distinguishes `DOMAIN_PROJECTION`, `GOVERNED_ASSERTION`, and `DISCOVERY_CANDIDATE` origins.

4. **EvidenceResolver — mandatory boundary**
   - Receives candidate objects only.
   - Resolves exact source references deterministically where possible.
   - Returns a resolvable research input or a rejection/insufficient-source result.
   - Is the only bridge toward later evidence/counterevidence workflow; it never accepts a vector score as evidence.

### 2.3 Six permanently isolated embedding spaces

| Space | Permitted candidate-discovery objective | Never implies |
|---|---|---|
| `VERSE_CONTEXT` | contextual textual neighbors and contrasts | semantic equivalence |
| `ROOT_CANDIDATE` | root-family candidates for inspection | root unity or semantic identity |
| `STRUCTURAL_PROFILE` | construction, morphology, valency, and participant-profile candidates | meaning equivalence |
| `CLAIM` | proposition/attribution-sensitive material candidates | claim truth/verification |
| `HYPOTHESIS` | support/challenge/counterevidence candidates | hypothesis confirmation/refutation |
| `EXTERNAL_RESEARCH` | bounded external-research query candidates | Quran-internal Blind-Lab evidence |

Enforce in contracts and storage:

```text
one query -> one space
one document -> one space
one judgment -> one space
one index namespace -> one space
no cross-space similarity, thresholds, rankings, or metric aggregation
```

A cross-space research need is six separate, visibly labeled retrieval calls followed by human synthesis—not a pooled vector query.

## 3. Canonical data and provenance design

### 3.1 Corpus resolver

LQE and Lisanapp must independently verify before Quran-dependent work:

```text
corpus_id: CANON-001
corpus_version: tanzil-uthmani-1.1
verse_count: 6236
sha256: ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af
```

Required behavior:

- resolve every Quran-derived item to an exact verse reference;
- store exact source text and source text hash;
- treat normalization as a separately declared, versioned, reversible derived view;
- fail closed for missing/mismatched corpus bytes;
- never let a copied corpus manifest imply Lisanapp production admission by itself.

### 3.2 Derived index record

Implement in Lisanapp a rebuildable record concept equivalent to:

```text
SemanticEmbedding
- id
- entity_type / entity_id
- embedding_space
- model_id / model_revision / tokenizer_revision
- preprocessing_revision
- source_revision / source_hash
- index_revision
- vector
- created_at
- stale_at / invalidation_reason
```

Rules:

- vector index deletion must not alter canonical data;
- model, tokenizer, preprocessing, source, or space changes invalidate relevant embeddings;
- every result carries model revision, space, source revision/hash, index revision, rank, and raw retrieval score;
- display score only as a `retrieval_score`, never confidence or semantic probability.

### 3.3 Candidate ledger and API envelope

Create an append-only Lisanapp `RetrievalCandidate` / retrieval-event record with:

```text
candidate_id, retrieval_event_id, space, source_layer,
query_text/hash, candidate entity/source refs,
model/tokenizer/index revisions, rank, raw_retrieval_score,
retrieval_reason, source provenance, timestamp,
status=CANDIDATE_FOR_REVIEW,
authority_notice=RETRIEVAL_OUTPUT_NOT_SEMANTIC_EVIDENCE
```

The API/UI must visibly distinguish `EXACT`, `VECTOR`, `GRAPH`, and `EXTERNAL` source layers.

## 4. LQE research and model-governance plan

### 4.1 Preserve the independently accepted seed

Preserve the reviewed LQE-T2 artifact unchanged:

```text
GOLD_SEED_V1
TRAINING_SEED_SET_INDEPENDENTLY_ACCEPTED
DATASET_EXPANSION_REQUIRED
```

Do not mutate the 36-example candidate to embed later review outcomes. Keep an independently versioned review artifact that binds reviewed SHA, source dataset hash, reviewer process, all dispositions, timestamp, and review-record hash.

### 4.2 Dataset expansion before training

Use the existing T3 plan as the first bounded expansion target:

- 396 total examples: 360 new plus preserved seed;
- 84 validation examples;
- 180 positive and 216 negative examples;
- 210 hard negatives;
- target space totals: `VERSE_CONTEXT` 60, `ROOT_CANDIDATE` 72, `STRUCTURAL_PROFILE` 72, `CLAIM` 66, `HYPOTHESIS` 60, `EXTERNAL_RESEARCH` 66.

Generation may mine Quran references, roots, lexical patterns, and structural forms only to **propose** candidates. It may not accept labels, rationales, contamination classes, or use embeddings/model ranks as ground truth.

Every new example must retain: stable ID, exact corpus binding, source references/text/hash, space, category, role, relevance, rationale, label origin, contamination class, Blind-Lab status, split, deterministic content hash, and independent review state.

High-risk categories (`CLAIM`, `HYPOTHESIS`, `EXTERNAL_RESEARCH`, proposition/polarity traps, and counterevidence candidates) require strengthened independent review.

### 4.3 Leakage and benchmark rules

Keep Benchmark v2 permanently frozen at:

`bc20c4dfc1a20200a034cf339e3b42be00d14d82d7b076f4fc36a8f9f6d555d4`

For expansion, reject:

- exact Quran-reference overlap with Benchmark v2;
- exact source-text/hash overlap;
- exact/reversed-pair reuse across train/validation;
- normalized Arabic text overlap;
- material lexical n-gram near duplicates;
- template-family reuse among synthetic queries;
- benchmark judgments reused as training labels;
- manual expansion tuned against observed Benchmark v2 failures.

Use non-model-based checks first; route suspicious near duplicates to independent human review. Do not use a candidate model as the sole leakage detector.

### 4.4 Provenance research before any model use

Continue the blocked-base decision. A base becomes `ELIGIBLE_BASE_CANDIDATE` only when the exact model and tokenizer revision have all mandatory evidence:

1. immutable model and tokenizer revisions;
2. architecture/objective identity;
3. named corpus categories and versions;
4. auditable source/release inventory and lineage;
5. licensing and distribution constraints;
6. filtering, deduplication, sampling, and preprocessing documentation;
7. explicit Quran/Tafsir/heritage/Islamic-QA exposure assessment;
8. explicit prior semantic supervision (STS/retrieval/NLI/QA) assessment;
9. no unresolved training components;
10. independent provenance review.

Current state remains:

```text
BASE_ARCHITECTURE_PROVENANCE_BLOCKED
BASE_SEARCH_CONTINUE
TRAINING_NOT_AUTHORIZED
```

The immediate research task is the authorized-to-propose, not-yet-authorized-to-execute, documentary review of HPLT Arabic provenance gaps. Do not download weights, train, fine-tune, create checkpoints, or adopt models during that task.

## 5. Implementation sequence

### Phase 0 — Governance and handoff contract

**Owner decision required before implementation:** approve an LQE-to-Lisanapp immutable handoff contract and a bounded R2 work package.

**Likely files in `LISAN-Quran-Embedding`:**
- Create `docs/architecture/LQE_LISANAPP_HANDOFF_CONTRACT.md`
- Create `schemas/lqe-lisanapp-handoff.schema.json`
- Create `models/manifests/lqe-handoff-capabilities.yaml`
- Test `tests/test_handoff_contract.py`

**Likely files in `lisanapp3`:**
- Create a canonical contract/reference, not a runtime dependency on LQE.
- Create Pydantic DTOs for immutable handoff import/verification.
- Add explicit refusal state for missing, stale, unqualified, or incompatible handoffs.

**Acceptance:** a handoff cannot claim model adoption, semantic authority, Blind-Lab eligibility, training authorization, or a Gate state.

### Phase 1 — R1 graph foundation in Lisanapp

Proceed only under the canonical R1 gate and a separately authorized Lisanapp work package.

- Implement rebuildable SQLite graph projection.
- Preserve origin/provenance and current four status axes.
- Add read-only API/read models and textual/table fallback before visual-only UI.
- Prove projection deletion does not mutate canonical records.
- Keep vector candidate edges distinct from governed relations.

**Exit:** `R1_VERIFIED_FOR_PROFILE`, not release acceptance.

### Phase 2 — R2 vector spike and contracts

Proceed only after R1 verification and separate R2 authorization.

- Run a `sqlite-vec` local spike against synthetic/non-production fixtures.
- Validate SQLite migration, vector serialization, rebuild lifecycle, per-space namespace enforcement, and performance for representative local data.
- Do not add Qdrant, Neo4j, microservices, LangChain, or external RAG frameworks.
- Add deterministic index-invalidation rules.
- Add `RetrievalCandidate` persistence and API response contracts.

**Required adversarial tests:** cross-space retrieval refusal; complete index deletion; stale model/source revision; no vector-to-Evidence transition; no vector-to-Gate transition; forbidden-source cache/index denial.

**Exit:** `sqlite-vec` becomes `ADOPTED_FOR_LOCAL_VECTOR_INDEX` only if the R2 spike acceptance criteria pass.

### Phase 3 — Candidate discovery integration

Proceed only after a provenance-qualified model is available for the intended profile. Until then, implement contracts, deterministic exact retrieval, and disabled/degraded vector UI states only.

- Build one index per permitted space from explicitly allowed source profiles.
- Enforce provenance policy at index-build time and query time.
- Return candidate envelopes with exact verse reference/text alongside vector provenance.
- Surface outputs in Semantic Differentiation Lab as **Candidate Neighbors**, never established relations.
- Ensure AIContextBuilder receives explicit labels: `CANONICAL_EVIDENCE`, `STRUCTURAL_EVIDENCE`, `VECTOR_CANDIDATE`, `GRAPH_CANDIDATE`, `EXTERNAL_CANDIDATE`.

**Exit:** R2 verification requires reproducibility, qualified model evaluation, isolation, candidate-only display, and representative performance.

### Phase 4 — R3 hybrid EvidenceResolver

Proceed only after R1 and R2 verification.

- Compose Exact + Vector + Graph retrieval as independently labeled result sets.
- Implement `EvidenceResolver` to resolve/reject candidates deterministically where possible.
- Preserve source-layer label and provenance through AI research runtime, counterevidence/falsification, and GateReport workflows.
- Prohibit any UI/API path that writes vector/graph candidates directly to canonical Evidence or claim status.

**Exit:** `R3_VERIFIED_FOR_PROFILE`, not adoption/release acceptance.

### Phase 5 — Controlled fine-tuning experiment (conditional)

This phase is **not currently authorized**. It is eligible for a separate owner decision only when all are true:

```text
expanded dataset independently accepted at sufficient scale
train/validation/Benchmark v2 separation passes
base architecture is provenance-qualified
exact model/tokenizer revisions pinned
Blind-Lab profile passes
reproducible training plan and external artifact root approved
explicit owner/governance authorization exists
```

If authorized: train outside Git; record code/dataset/model/tokenizer/index/environment hashes, seeds, stopped-run policy, checkpoints externally, per-space metrics, frozen Benchmark v2 results, and contamination-control results. The maximum outcome is `MODEL_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW`.

## 6. Operational runbook

1. Reviewer chooses one declared research objective and one embedding space.
2. System validates profile and source-policy eligibility.
3. Exact retrieval runs first and returns source-resolved material where available.
4. The permitted per-space index retrieves top-k **candidates** using a pinned index/model revision.
5. Candidate ledger records query, profile, revisions, score, rank, source refs, and authority notice.
6. UI presents exact source text, corpus hash, provenance, space, score, and visible `candidate only` status.
7. Reviewer resolves relevant candidates against admitted Corpus and applicable methodology through existing Lisan workflow.
8. Any research conclusion, evidence, counterevidence, GateReport, or status action occurs outside the embedding system and follows canonical governance.
9. Index/source/model changes invalidate affected derived outputs and require rebuild/re-evaluation.

### Blind-Lab operating rule

Before valid Internal Lock, retrieval can access only the sources allowed for the active Blind-Lab profile. Forbidden Tafsir, heritage, Islamic-QA, external research, prior conclusions, dictionaries, and derived caches/embeddings must be excluded from:

- index construction;
- query filtering;
- graph projection;
- candidate ledger lookup;
- AI context construction;
- UI/API responses;
- persistent cache reuse.

With no eligible base architecture, vector operation for Blind-Lab-sensitive use remains disabled. The app must show an honest `MODEL_OR_PROVENANCE_UNAVAILABLE` degraded state rather than fabricating vectors or silently falling back to a prohibited model.

## 7. Verification and acceptance plan

### LQE verification

- exact CANON-001 artifact/hash/count resolution;
- deterministic candidate and manifest regeneration from clean checkout;
- schema/hash and provenance contract tests;
- train/validation/benchmark exact and near-duplicate leakage tests;
- independent per-example review records;
- model provenance matrix validation;
- no tracked model weights/checkpoints;
- pytest + Ruff, then expanded checks as the project adopts them.

### Lisanapp R1–R3 verification

- unit/property tests for state and authority invariants;
- Alembic migration/model parity and rollback validation;
- API/OpenAPI and typed frontend contract checks;
- index rebuild and deletion safety;
- model/source/index staleness invalidation;
- cross-space rejection;
- Blind-Lab cache/index/prompt isolation attacks;
- candidate-to-Evidence and candidate-to-Gate negative tests;
- browser E2E for candidate labels, provenance display, degraded mode, and textual/table fallback;
- affected backend suite, Ruff, Pyright, frontend build, contract checks, and adversarial tests at phase closure.

## 8. Explicit non-recommendations

Do not:

- couple Lisanapp runtime to the LQE repository;
- use a universal Quranic embedding score;
- use vector similarity as a truth/authority/proof field;
- use a model merely because it is Arabic, popular, local, or scores well in a few examples;
- allow contaminated or undocumented pretrained weights/tokenizer into Blind-Lab-sensitive operation;
- introduce Qdrant Server, Neo4j, microservices, LangChain, Haystack, or LlamaIndex for core Quranic retrieval;
- mix `EXTERNAL_RESEARCH` vectors with Quran-internal indexes;
- tune a candidate dataset or thresholds after seeing Benchmark v2 outcomes;
- start from scratch training as a casual workaround for missing model provenance.

## 9. Decision summary

This plan is suitable because it achieves useful retrieval assistance while preserving the canonical Lisan requirement:

> Retrieval discovers candidates. Evidence resolves them. Governance decides what can become governed knowledge.

Current actionable sequence:

1. Preserve LQE-T2 gold seed and execute only the separately authorized LQE-T3-R1 documentary provenance-gap review.
2. Obtain owner authorization for the LQE-to-Lisanapp immutable handoff contract and the next gated Lisanapp phase.
3. Complete Lisanapp R1 graph foundation before R2 vector runtime.
4. Expand and independently review training data without training.
5. Identify a provenance-qualified base or retain the block.
6. Run the R2 local vector spike only under the canonical gate.
7. Consider controlled training only after all data, provenance, separation, reproducibility, and owner-authorization prerequisites are independently satisfied.

## Risks and owner decisions

| Topic | Recommendation | Decision owner |
|---|---|---|
| General-language pretraining with incomplete source inventory | Keep fail-closed for Blind-Lab-sensitive use | Owner/governance only, if reconsidered |
| LQE-to-Lisanapp integration | Immutable handoff only; no runtime dependency | Owner approval of bounded work package |
| sqlite-vec | Evaluate locally in R2; adopt only after spike gates pass | R2 acceptance authority |
| External research retrieval | Isolated index/profile, never mixed with Quran-internal Blind Lab | Future separately authorized work package |
| Training | Remain blocked until all listed prerequisites pass | Explicit owner/governance authorization |
| Training from scratch | Feasibility study only after data/hardware/maintenance evidence | Owner/governance decision |

---

## Files likely to change when implementation is separately authorized

**LQE repository (`D:\APP\tafseer\LISAN-Quran-Embedding`)**

- `docs/governance/BASE_ARCHITECTURE_PROVENANCE_POLICY.md`
- `models/manifests/base-architecture-provenance.yaml`
- `data/training/lqe-t3-expansion-plan.v1.0.0.yaml`
- `docs/governance/LQE_T3_DATASET_EXPANSION_POLICY.md`
- `docs/architecture/LQE_T3_EXPANSION_DESIGN.md`
- New handoff contract/schema/tests as described in Phase 0.

**Lisanapp repository (`D:\APP\tafseer\lisanapp3`)**

- New incremental Alembic migrations only; never modify initial squash migration.
- Backend retrieval-candidate, vector-index, provenance, and EvidenceResolver contracts/services/routes.
- SQLite-derived graph/index lifecycle services.
- Typed frontend query clients and candidate-only UI states.
- Canonical retrieval documentation references, affected UI/backend contract matrix entries, and focused test suites.

No implementation starts from this plan alone.
