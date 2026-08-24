# R2 Vector Benchmark Decision

Status: `EMBEDDING_MODEL_SELECTION_BLOCKED`

This is evaluation evidence, not semantic authority, independent review, or
R2 completion. It applies to runner + model manifest + corpus input SHA-256
`2c6f22ff2ee31299c0342aa53d097fb1990880decabc56385920b1cb622b9d25`.

## Acceptance-to-evidence map at the stop boundary

| Canonical R2 acceptance | Artifact/evidence | Verdict |
|---|---|---|
| Reproducible benchmark | `cases.json`, `models.json`, `run_benchmark.py`, exact model revisions, deterministic CPU configuration | PASSED; two complete runs produced identical result SHA-256 |
| Model qualifies under documented metrics | `results.json`, per-space thresholds predeclared in `models.json` | BLOCKED; no candidate qualified in every space |
| Rebuildable vector index | Not implemented after the model-selection stop condition | NOT_VERIFIED |
| Canonical knowledge survives index deletion | Not implemented after the model-selection stop condition | NOT_VERIFIED |
| Source/model revisions recorded | Benchmark model revisions and corpus provenance are recorded; runtime embedding provenance is not implemented | PARTIAL |
| Incompatible spaces rejected | Six benchmark spaces are isolated in evaluation; runtime rejection is not implemented | PARTIAL |
| Candidates visibly labeled | Benchmark authority notice exists; API/UI are not implemented | NOT_VERIFIED |
| Candidates cannot enter Evidence directly | Benchmark is structurally separate and explicitly non-authoritative; runtime path is not implemented | PARTIAL |
| Blind Lab cannot leak forbidden indexed sources | No runtime index exists; adversarial runtime proof not executed | NOT_VERIFIED |
| Representative local performance acceptable | No runtime sqlite-vec index exists; performance Spike not executed | NOT_VERIFIED |

The incomplete mandatory items prevent `R2_VERIFIED_FOR_PROFILE` and prevent a
candidate SHA from being ready for independent R2 review.

## Corpus summary

- Six separately evaluated spaces: `VERSE_CONTEXT`, `STRUCTURAL_PROFILE`,
  `HYPOTHESIS`, `CLAIM`, `ROOT_CANDIDATE`, and `EXTERNAL_RESEARCH`.
- 30 candidate documents and 12 queries.
- Coverage includes known-close candidates, known non-neighbors, difficult
  lexical distinctions, contextual outliers, candidate counterevidence, and
  false-positive traps.
- Quranic fragments are retained exactly from existing repository fixtures:
  `tests/test_corpus_adapter.py:26` and `tests/test_slice_b.py:71`. They remain
  test fixtures and are not promoted to canonical Corpus evidence.
- Every other case is explicitly labeled synthetic or external-fixture data.

## Candidate models

| Candidate | Exact revision | Profile |
|---|---|---|
| `intfloat/multilingual-e5-small` | `614241f622f53c4eeff9890bdc4f31cfecc418b3` | multilingual E5, 384 dimensions, query/passage prefixes |
| `Omartificial-Intelligence-Space/E5-all-nli-triplet-Matryoshka` | `fa55cb14c32088a13bc7af8f8b2149e4da8c9742` | Arabic NLI E5 fine-tune, 384 dimensions |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | `e8f8c211226b894fcb81acc59f3b34ba3efd5f42` | multilingual paraphrase model, 384 dimensions |

All models ran locally on CPU with `trust_remote_code=false`, L2-normalized
float embeddings, and `top_k=3`.

Two complete cached executions produced the identical machine-readable result
SHA-256:
`DC2F6F6B353773BA2E1DDFAC618F51B8C21E401E2ED9A8B1A16E89CDCC575B56`.

## Macro metrics

| Candidate | Recall@3 | Precision@3 | MRR | nDCG@3 | FPR | Qualifies |
|---|---:|---:|---:|---:|---:|---|
| multilingual E5 small | 0.750000 | 0.388889 | 0.708333 | 0.687701 | 0.333333 | No |
| Arabic E5 NLI Matryoshka | 0.916667 | 0.472222 | 0.881945 | 0.852049 | 0.333333 | No |
| paraphrase multilingual MiniLM | 0.833333 | 0.416667 | 0.808333 | 0.751876 | 0.416667 | No |

## Per-space nDCG@3 / blocker signal

| Space | multilingual E5 | Arabic E5 | paraphrase MiniLM | Relevant blocker |
|---|---:|---:|---:|---|
| `CLAIM` | 0.329501 | 0.500000 | 0.576113 | No candidate met the per-space gate |
| `EXTERNAL_RESEARCH` | 0.793441 | 0.898354 | 0.453171 | Arabic E5 qualified |
| `HYPOTHESIS` | 0.521296 | 0.981970 | 0.981970 | Arabic E5 and MiniLM qualified |
| `ROOT_CANDIDATE` | 0.981970 | 0.981970 | 1.000000 | First two had FPR 1.0; MiniLM qualified |
| `STRUCTURAL_PROFILE` | 0.500000 | 0.750000 | 0.500000 | No candidate met every per-space gate |
| `VERSE_CONTEXT` | 1.000000 | 1.000000 | 1.000000 | All candidates qualified |

The leading Arabic E5 model is not adopted: strong aggregate performance does
not cure its failures in `CLAIM`, `STRUCTURAL_PROFILE`, and the
`ROOT_CANDIDATE` false-positive trap.

## sqlite-vec evaluation state

`sqlite-vec==0.1.9` was resolved and imported under Python 3.12 / SQLite
3.49.1 as a development evaluation dependency. The R2 Spike, persistence,
filtering, rebuild, recovery, and local performance profile were not executed
because model selection hit the authorized stop condition first.

Result: `INSTALLED_FOR_EVALUATION_NOT_EVALUATED`; canonical status remains
`APPROVED_FOR_EVALUATION`. No production adoption was recorded.

## Executed commands

```text
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -r backend\requirements-dev.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m pytest tools\governance-lab\vector-benchmark\r2\test_benchmark_contract.py -q
.venv\Scripts\python.exe -m ruff check tools\governance-lab\vector-benchmark\r2\run_benchmark.py tools\governance-lab\vector-benchmark\r2\test_benchmark_contract.py
.venv\Scripts\python.exe tools\governance-lab\vector-benchmark\r2\run_benchmark.py
.venv\Scripts\python.exe tools\governance-lab\vector-benchmark\r2\run_benchmark.py --output <unique-temporary-file>
Get-FileHash tools\governance-lab\vector-benchmark\r2\results.json -Algorithm SHA256
Get-FileHash <unique-temporary-file> -Algorithm SHA256
```

## Official implementation sources

- sqlite-vec Python loading and float32 representation:
  https://alexgarcia.xyz/sqlite-vec/python.html
- sqlite-vec virtual-table KNN contract:
  https://alexgarcia.xyz/sqlite-vec/
- Sentence Transformers revision pinning and normalized encoding:
  https://www.sbert.net/docs/package_reference/sentence_transformer/model.html
- Candidate model cards:
  https://huggingface.co/intfloat/multilingual-e5-small
  https://huggingface.co/Omartificial-Intelligence-Space/E5-all-nli-triplet-Matryoshka
  https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

## Decision boundary and exact next action

Do not lower thresholds, relabel cases, select the macro leader, or implement a
default model without governed review. Independent architecture review must
choose whether to:

1. expand the candidate-model set for the failing `CLAIM` and
   `STRUCTURAL_PROFILE` spaces;
2. authorize different models by embedding space; or
3. revise the benchmark corpus/thresholds with an explicit rationale before a
   new run.

R3 and V4 remain not started.
