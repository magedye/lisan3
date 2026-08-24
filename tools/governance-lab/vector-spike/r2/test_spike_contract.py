import json
from pathlib import Path

SPIKE_ROOT = Path(__file__).parent


def test_committed_spike_result_preserves_evaluation_boundary():
    result = json.loads((SPIKE_ROOT / "results.json").read_text(encoding="utf-8"))
    assert result["status"] == "SQLITE_VEC_EVALUATION_PASSED"
    assert result["canonical_adoption_status"] == "APPROVED_FOR_EVALUATION"
    assert result["embedding_model_selection"] == "EMBEDDING_MODEL_SELECTION_BLOCKED"
    assert result["production_vector_state"] == "NOT_CREATED"
    assert result["provenance_class"] == "SYNTHETIC_EVALUATION"
    assert all(result["checks"].values())
    assert result["performance_passed"] is True


def test_spike_profile_and_thresholds_are_explicit():
    result = json.loads((SPIKE_ROOT / "results.json").read_text(encoding="utf-8"))
    assert result["profile"] == {
        "dimensions": 32,
        "query_runs": 100,
        "top_k": 10,
        "vector_count": 5_000,
    }
    assert result["predeclared_performance_thresholds"] == {
        "max_build_seconds": 5.0,
        "max_query_p95_milliseconds": 100.0,
    }
