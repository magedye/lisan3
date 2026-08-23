from dataclasses import FrozenInstanceError
from types import SimpleNamespace

from backend.domain.services.corpus import authority


def test_corpus_authority_decision_matrix():
    def distinct(value: str) -> str:
        return (" " + value).strip()

    source_id = "TANZIL_QURAN_UTHMANI"
    original = authority.CANONICAL_CORPUS_ADMISSIONS[source_id]
    active = authority.CorpusAdmissionRecord(
        source_id=source_id,
        source_role_status=distinct(authority.SOURCE_ROLE_APPROVED),
        expected_hash=distinct("b" * 64),
        artifact_verification_status=distinct(authority.HASH_VERIFIED),
        activation_status=distinct(authority.PRODUCTION_ACTIVE),
        authority_reference="canonical:test",
    )

    def snapshot(**overrides):
        values = {
            "canonical_text_source": source_id,
            "canonical_text_hash": distinct("b" * 64),
            "source_role_status": distinct(authority.SOURCE_ROLE_APPROVED),
            "artifact_presence_status": distinct(authority.ARTIFACT_PRESENT),
            "expected_canonical_text_hash": distinct("b" * 64),
            "hash_verification_status": distinct(authority.HASH_VERIFIED),
            "import_validation_status": distinct(authority.IMPORT_VALIDATED),
            "activation_status": distinct(authority.PRODUCTION_ACTIVE),
            "artifact_provenance": "canonical:test",
            "fixture_only": False,
            "validation_status": distinct("VALIDATED"),
        }
        values.update(overrides)
        return SimpleNamespace(**values)

    authority.CANONICAL_CORPUS_ADMISSIONS[source_id] = active
    try:
        valid = snapshot()
        assert authority.production_validation_failures(valid) == []
        assert authority.is_production_validated(valid) is True
        try:
            active.source_id = "MUTATED"
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("Canonical admission records must remain immutable")

        cases = [
            ({"canonical_text_source": "AAA_UNKNOWN"}, "no admission record"),
            ({"canonical_text_source": "ZZZ_UNKNOWN"}, "no admission record"),
            ({"source_role_status": "AAA_INVALID"}, "source-role approval"),
            ({"source_role_status": "ZZZ_INVALID"}, "source-role approval"),
            ({"artifact_presence_status": "AAA_INVALID"}, "artifact presence"),
            ({"artifact_presence_status": "ZZZ_INVALID"}, "artifact presence"),
            ({"expected_canonical_text_hash": "a" * 64}, "authority-bound"),
            ({"expected_canonical_text_hash": "c" * 64}, "authority-bound"),
            ({"canonical_text_hash": "a" * 64}, "does not match"),
            ({"canonical_text_hash": "c" * 64}, "does not match"),
            ({"hash_verification_status": "AAA_INVALID"}, "not verified"),
            ({"hash_verification_status": "ZZZ_INVALID"}, "not verified"),
            ({"import_validation_status": "AAA_INVALID"}, "has not passed"),
            ({"import_validation_status": "ZZZ_INVALID"}, "has not passed"),
            ({"activation_status": "AAA_INVALID"}, "not production-active"),
            ({"activation_status": "ZZZ_INVALID"}, "not production-active"),
            ({"artifact_provenance": None}, "provenance is missing"),
            ({"artifact_provenance": ""}, "provenance is missing"),
            ({"fixture_only": True}, "test fixtures"),
        ]
        for overrides, expected_fragment in cases:
            failures = authority.production_validation_failures(snapshot(**overrides))
            assert any(expected_fragment in failure for failure in failures)

        assert (
            authority.is_production_validated(snapshot(validation_status="AAA_INVALID"))
            is False
        )
        assert (
            authority.is_production_validated(snapshot(validation_status="ZZZ_INVALID"))
            is False
        )

        for invalid_status in ("AAA_INVALID", "ZZZ_INVALID"):
            authority.CANONICAL_CORPUS_ADMISSIONS[source_id] = (
                authority.CorpusAdmissionRecord(
                    source_id=source_id,
                    source_role_status=invalid_status,
                    expected_hash=distinct("b" * 64),
                    artifact_verification_status=authority.HASH_VERIFIED,
                    activation_status=authority.PRODUCTION_ACTIVE,
                    authority_reference="canonical:test",
                )
            )
            assert any(
                "source role is not approved" in item
                for item in authority.production_validation_failures(snapshot())
            )

            authority.CANONICAL_CORPUS_ADMISSIONS[source_id] = (
                authority.CorpusAdmissionRecord(
                    source_id=source_id,
                    source_role_status=authority.SOURCE_ROLE_APPROVED,
                    expected_hash=distinct("b" * 64),
                    artifact_verification_status=authority.HASH_VERIFIED,
                    activation_status=invalid_status,
                    authority_reference="canonical:test",
                )
            )
            assert any(
                "canonical admission is not production-active" in item
                for item in authority.production_validation_failures(snapshot())
            )

        authority.CANONICAL_CORPUS_ADMISSIONS[source_id] = original
        pending = authority.production_validation_failures(snapshot())
        assert any("no authority-bound expected hash" in item for item in pending)
        assert any("not production-active" in item for item in pending)
    finally:
        authority.CANONICAL_CORPUS_ADMISSIONS[source_id] = original


if __name__ == "__main__":
    test_corpus_authority_decision_matrix()
