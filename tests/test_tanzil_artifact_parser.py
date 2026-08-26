import hashlib
import json
import unicodedata
from collections import Counter
from dataclasses import replace

import pytest

from backend.domain.services.corpus.authority import get_canonical_admission
from backend.domain.services.corpus.tanzil import TanzilArtifactParser
from backend.infrastructure.database import REPOSITORY_ROOT

RAW_PATH = REPOSITORY_ROOT / "data/corpus/tanzil/tanzil-uthmani-1.1.txt"
INDEX_PATH = REPOSITORY_ROOT / "data/corpus/tanzil/quran-verse-index-v1.0.json"


def _admission():
    admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
    assert admission is not None
    return admission


def _authority_for(raw_bytes: bytes, index: dict, **overrides):
    index_bytes = json.dumps(index, ensure_ascii=False).encode("utf-8")
    values = {
        "expected_hash": hashlib.sha256(raw_bytes).hexdigest(),
        "expected_bytes": len(raw_bytes),
        "identity_index_sha256": hashlib.sha256(index_bytes).hexdigest(),
    }
    values.update(overrides)
    return replace(_admission(), **values), index_bytes


def test_real_tanzil_artifact_reconciles_every_canonical_identity():
    raw_bytes = RAW_PATH.read_bytes()
    result = TanzilArtifactParser(_admission()).parse(
        raw_bytes, INDEX_PATH.read_bytes()
    )

    assert len(result.verses) == 6_236
    assert {verse.surah for verse in result.verses} == set(range(1, 115))
    assert len({verse.verse_ref for verse in result.verses}) == 6_236
    assert Counter(verse.surah for verse in result.verses)[2] == 286
    assert result.verses[0].verse_ref == "1:1"
    assert result.verses[-1].verse_ref == "114:6"

    physical_lines = raw_bytes.split(b"\n")[:-1]
    for verse in result.verses:
        assert verse.text.encode("utf-8") == physical_lines[verse.line_number - 1]


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data[:-1],
        lambda data: data + "آية زائدة\n".encode(),
        lambda data: unicodedata.normalize(
            "NFC", data.decode("utf-8")
        ).encode("utf-8"),
    ],
    ids=("truncated", "extra-record", "unicode-normalized"),
)
def test_changed_tanzil_bytes_fail_the_authority_bound_hash(mutate):
    with pytest.raises(ValueError, match="artifact hash mismatch"):
        TanzilArtifactParser(_admission()).parse(
            mutate(RAW_PATH.read_bytes()), INDEX_PATH.read_bytes()
        )


def test_malformed_utf8_fails_even_under_a_matching_test_authority():
    raw_bytes = RAW_PATH.read_bytes().replace(
        "بِسْمِ".encode(), b"\xff", 1
    )
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    admission, index_bytes = _authority_for(raw_bytes, index)

    with pytest.raises(ValueError, match="not valid UTF-8"):
        TanzilArtifactParser(admission).parse(raw_bytes, index_bytes)


def test_malformed_record_fails_even_under_a_matching_test_authority():
    raw_bytes = RAW_PATH.read_bytes().replace(
        "بِسْمِ".encode(), b"\t" + "بِسْمِ".encode(), 1
    )
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    admission, index_bytes = _authority_for(raw_bytes, index)

    with pytest.raises(ValueError, match="Malformed Tanzil record"):
        TanzilArtifactParser(admission).parse(raw_bytes, index_bytes)


def test_wrong_authority_verse_count_fails_closed():
    with pytest.raises(ValueError, match="verse_count does not match authority"):
        TanzilArtifactParser(
            replace(_admission(), expected_verse_count=6_235)
        ).parse(RAW_PATH.read_bytes(), INDEX_PATH.read_bytes())


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda index: index["surahs"][0]["verses"][1].update(
                {"line": index["surahs"][0]["verses"][0]["line"]}
            ),
            "duplicate",
        ),
        (
            lambda index: index["surahs"][0]["verses"].pop(),
            "missing or extra identities",
        ),
        (
            lambda index: index["surahs"].reverse(),
            "missing or out of order",
        ),
    ],
    ids=("duplicate", "missing", "impossible-order"),
)
def test_invalid_verse_identity_indexes_fail_closed(mutation, message):
    raw_bytes = RAW_PATH.read_bytes()
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    mutation(index)
    admission, index_bytes = _authority_for(raw_bytes, index)

    with pytest.raises(ValueError, match=message):
        TanzilArtifactParser(admission).parse(raw_bytes, index_bytes)


def test_wrong_source_or_version_cannot_use_tanzil_parser():
    raw_bytes = RAW_PATH.read_bytes()
    index_bytes = INDEX_PATH.read_bytes()
    with pytest.raises(ValueError, match="Wrong canonical source"):
        TanzilArtifactParser(replace(_admission(), source_id="OTHER")).parse(
            raw_bytes, index_bytes
        )
    with pytest.raises(ValueError, match="Wrong canonical Tanzil version"):
        TanzilArtifactParser(
            replace(_admission(), canonical_text_version="0.0")
        ).parse(raw_bytes, index_bytes)
