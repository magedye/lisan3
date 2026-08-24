import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPACES = {
    "VERSE_CONTEXT",
    "STRUCTURAL_PROFILE",
    "HYPOTHESIS",
    "CLAIM",
    "ROOT_CANDIDATE",
    "EXTERNAL_RESEARCH",
}
REQUIRED_CASE_TYPES = {
    "KNOWN_CLOSE",
    "KNOWN_NON_NEIGHBOR",
    "DIFFICULT_LEXICAL_DISTINCTION",
    "CONTEXTUAL_OUTLIER",
    "CANDIDATE_COUNTEREVIDENCE",
    "FALSE_POSITIVE_TRAP",
}


def test_benchmark_corpus_is_complete_traceable_and_non_authoritative():
    corpus = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    assert set(corpus["spaces"]) == SPACES
    assert "not Quranic semantic evidence" in corpus["authority_notice"]
    case_types: set[str] = set()
    for space in corpus["spaces"].values():
        document_ids = {item["id"] for item in space["documents"]}
        assert len(document_ids) == len(space["documents"])
        for document in space["documents"]:
            assert document["text"]
            assert document["provenance"]
            assert document["source_role"] in {
                "TEST_FIXTURE",
                "SYNTHETIC",
                "EXTERNAL_FIXTURE",
            }
        for query in space["queries"]:
            assert set(query["relevance"]).issubset(document_ids)
            assert set(query["false_positive_traps"]).issubset(document_ids)
            assert not set(query["relevance"]).intersection(
                query["false_positive_traps"]
            )
            case_types.update(query["case_types"])
    assert REQUIRED_CASE_TYPES.issubset(case_types)


def test_model_manifest_pins_revisions_and_predeclares_selection():
    manifest = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))
    assert manifest["output_dimension"] == 384
    assert manifest["top_k"] == 3
    assert len(manifest["candidates"]) >= 3
    for candidate in manifest["candidates"]:
        assert len(candidate["model_revision"]) == 40
        assert candidate["trust_remote_code"] is False
    assert manifest["selection_policy"]["material_tie"]


def test_partial_candidate_runs_cannot_select_a_model(tmp_path):
    import subprocess
    import sys

    output = tmp_path / "partial.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_benchmark.py"),
            "--candidate-id",
            "missing-candidate",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert not output.exists()


def test_empty_candidate_filter_means_the_complete_manifest():
    manifest = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location(
        "r2_benchmark", ROOT / "run_benchmark.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    candidates = module._select_candidates(manifest["candidates"], set())
    assert len(candidates) == len(manifest["candidates"])


def test_committed_results_match_current_runner_manifest_and_corpus():
    manifest = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256()
    for path in (ROOT / "run_benchmark.py", ROOT / "models.json", ROOT / "cases.json"):
        digest.update(path.read_bytes())
    assert results["input_sha256"] == digest.hexdigest()
    assert results["complete_candidate_set"] is True
    assert {item["candidate_id"] for item in results["results"]} == {
        item["id"] for item in manifest["candidates"]
    }
    assert {item["embedding_dimension"] for item in results["results"]} == {384}
    assert results["decision"]["status"] == "EMBEDDING_MODEL_SELECTION_BLOCKED"
