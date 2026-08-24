"""Run the deterministic, non-authoritative R2 embedding benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash_inputs(*paths: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _dcg(grades: list[int]) -> float:
    return sum(
        (2**grade - 1) / math.log2(index + 2) for index, grade in enumerate(grades)
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _select_candidates(
    candidates: list[dict[str, Any]], requested: set[str]
) -> list[dict[str, Any]]:
    selected = [
        candidate
        for candidate in candidates
        if not requested or candidate["id"] in requested
    ]
    if requested and requested != {candidate["id"] for candidate in selected}:
        raise ValueError("unknown candidate ID")
    return selected


def _evaluate_space(
    model: SentenceTransformer,
    model_config: dict[str, Any],
    space: dict[str, Any],
    top_k: int,
) -> dict[str, float | int]:
    documents = sorted(space["documents"], key=lambda item: item["id"])
    queries = sorted(space["queries"], key=lambda item: item["id"])
    document_vectors = model.encode(
        [model_config["document_prefix"] + item["text"] for item in documents],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    query_vectors = model.encode(
        [model_config["query_prefix"] + item["text"] for item in queries],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    recalls: list[float] = []
    precisions: list[float] = []
    reciprocal_ranks: list[float] = []
    ndcgs: list[float] = []
    false_positive_rates: list[float] = []
    for query, vector in zip(queries, query_vectors, strict=True):
        scores = document_vectors @ vector
        ranked = sorted(
            zip(documents, scores, strict=True),
            key=lambda item: (-float(item[1]), item[0]["id"]),
        )
        ranked_ids = [item[0]["id"] for item in ranked]
        retrieved = ranked_ids[:top_k]
        relevant = query["relevance"]
        relevant_retrieved = [item for item in retrieved if item in relevant]
        recalls.append(len(relevant_retrieved) / len(relevant))
        precisions.append(len(relevant_retrieved) / top_k)
        first_rank = next(
            (
                index
                for index, item in enumerate(ranked_ids, start=1)
                if item in relevant
            ),
            None,
        )
        reciprocal_ranks.append(0.0 if first_rank is None else 1.0 / first_rank)
        actual_grades = [int(relevant.get(item, 0)) for item in retrieved]
        ideal_grades = sorted(
            (int(value) for value in relevant.values()), reverse=True
        )[:top_k]
        ideal_dcg = _dcg(ideal_grades)
        ndcgs.append(0.0 if ideal_dcg == 0 else _dcg(actual_grades) / ideal_dcg)
        traps = set(query["false_positive_traps"])
        false_positive_rates.append(len(traps.intersection(retrieved)) / len(traps))
    return {
        "query_count": len(queries),
        "document_count": len(documents),
        "recall_at_k": round(_mean(recalls), 6),
        "precision_at_k": round(_mean(precisions), 6),
        "mrr": round(_mean(reciprocal_ranks), 6),
        "ndcg_at_k": round(_mean(ndcgs), 6),
        "false_positive_rate": round(_mean(false_positive_rates), 6),
    }


def _qualifies(result: dict[str, Any], policy: dict[str, Any]) -> bool:
    required = policy["required_per_space"]
    return all(
        metrics["recall_at_k"] >= required["recall_at_k"]
        and metrics["mrr"] >= required["mrr"]
        and metrics["ndcg_at_k"] >= required["ndcg_at_k"]
        and metrics["false_positive_rate"] <= required["false_positive_rate"]
        for metrics in result["spaces"].values()
    )


def _decision(results: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    qualified = [item for item in results if item["qualifies"]]
    if not qualified:
        return {
            "status": "EMBEDDING_MODEL_SELECTION_BLOCKED",
            "reason": "no candidate satisfied every per-space threshold",
        }
    ranked = sorted(
        qualified, key=lambda item: (-item["macro"]["ndcg_at_k"], item["candidate_id"])
    )
    if len(ranked) == 1:
        return {
            "status": "SELECTED",
            "candidate_id": ranked[0]["candidate_id"],
            "reason": "only qualifying candidate",
        }
    first, second = ranked[:2]
    delta = first["macro"]["ndcg_at_k"] - second["macro"]["ndcg_at_k"]
    leaders = {first["candidate_id"]: 0, second["candidate_id"]: 0}
    for space in first["spaces"]:
        first_score = first["spaces"][space]["ndcg_at_k"]
        second_score = second["spaces"][space]["ndcg_at_k"]
        if first_score > second_score:
            leaders[first["candidate_id"]] += 1
        elif second_score > first_score:
            leaders[second["candidate_id"]] += 1
    if delta < 0.02 or (delta < 0.05 and min(leaders.values()) >= 2):
        return {
            "status": "EMBEDDING_MODEL_SELECTION_BLOCKED",
            "reason": "top candidates are materially tied under the predeclared policy",
            "boundary": {
                "first": first["candidate_id"],
                "second": second["candidate_id"],
                "macro_ndcg_delta": round(delta, 6),
                "space_leads": leaders,
            },
        }
    return {
        "status": "SELECTED",
        "candidate_id": first["candidate_id"],
        "reason": "highest qualifying macro nDCG@K outside the material-tie boundary",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=Path, default=ROOT / "models.json")
    parser.add_argument("--cases", type=Path, default=ROOT / "cases.json")
    parser.add_argument("--output", type=Path, default=ROOT / "results.json")
    parser.add_argument("--candidate-id", action="append", default=[])
    args = parser.parse_args()
    manifest = _load(args.models)
    corpus = _load(args.cases)
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True, warn_only=True)
    requested = set(args.candidate_id)
    try:
        candidates = _select_candidates(manifest["candidates"], requested)
    except ValueError:
        parser.error("unknown --candidate-id")
    results: list[dict[str, Any]] = []
    for candidate in candidates:
        print(f"MODEL_START={candidate['id']}", flush=True)
        model = SentenceTransformer(
            candidate["model_name"],
            revision=candidate["model_revision"],
            trust_remote_code=candidate["trust_remote_code"],
            device="cpu",
            truncate_dim=manifest["output_dimension"],
        )
        embedding_dimension = model.get_embedding_dimension()
        if embedding_dimension is None:
            raise RuntimeError(
                f"Model {candidate['id']} did not declare an embedding dimension"
            )
        print(
            f"MODEL_LOADED={candidate['id']} DIMENSION={embedding_dimension}",
            flush=True,
        )
        spaces = {
            name: _evaluate_space(model, candidate, space, manifest["top_k"])
            for name, space in sorted(corpus["spaces"].items())
        }
        macro_keys = (
            "recall_at_k",
            "precision_at_k",
            "mrr",
            "ndcg_at_k",
            "false_positive_rate",
        )
        result: dict[str, Any] = {
            "candidate_id": candidate["id"],
            "model_name": candidate["model_name"],
            "model_revision": candidate["model_revision"],
            "embedding_dimension": embedding_dimension,
            "spaces": spaces,
            "macro": {
                key: round(_mean([float(item[key]) for item in spaces.values()]), 6)
                for key in macro_keys
            },
        }
        result["qualifies"] = _qualifies(result, manifest["selection_policy"])
        results.append(result)
        print(f"MODEL_EVALUATED={candidate['id']}", flush=True)
        del model
    complete_candidate_set = len(candidates) == len(manifest["candidates"])
    decision = (
        _decision(results, manifest["selection_policy"])
        if complete_candidate_set
        else {
            "status": "EMBEDDING_MODEL_SELECTION_BLOCKED",
            "reason": "candidate set is incomplete; partial runs are evidence inputs only",
        }
    )
    payload = {
        "schema_version": "R2_BENCHMARK_RESULTS_V1",
        "authority_notice": corpus["authority_notice"],
        "input_sha256": _hash_inputs(Path(__file__), args.models, args.cases),
        "top_k": manifest["top_k"],
        "normalization": manifest["normalization"],
        "complete_candidate_set": complete_candidate_set,
        "results": results,
        "decision": decision,
    }
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload["decision"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
