"""Generate and verify the bounded QAC Stage-A evidence package."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import unicodedata
from itertools import pairwise
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "docs" / "evidence" / "qac-stage-a-2026-08-27"
STARTING_SHA = "d69d1cadc9c13ccf542b4ebc25e358f7a7846052"
EXPECTED_QAC_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
EXPECTED_QAC_BYTES = 6_309_503
EXPECTED_QAC_RECORDS = 128_219
EXPECTED_QAC_WORDS = 77_429
EXPECTED_QAC_VERSES = 6_236
EXPECTED_QAC_SURAHS = 114
CONTINUATION_RESULT = "QAC_STAGE_A_OFFICIAL_BINDING_AND_LICENSE_BLOCKED"
OFFICIAL_BINDING_ATTEMPTED_AT_UTC = "2026-08-26T23:50:10.7789646Z"
QAC_HEADER = "LOCATION\tFORM\tTAG\tFEATURES"
LOCATION_PATTERN = re.compile(r"^\((\d+):(\d+):(\d+):(\d+)\)$")
PROHIBITED_FEATURE_MARKERS = (
    "GLOSS",
    "TRANSLATION",
    "SEMANTIC",
    "SEM:",
    "ONTOLOGY",
    "MEANING",
    "CONFIDENCE",
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_text(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _parse_qac(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) != EXPECTED_QAC_BYTES or _sha256(raw) != EXPECTED_QAC_SHA256:
        raise ValueError(
            "QAC candidate bytes do not match the Stage-A candidate identity"
        )
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("QAC candidate unexpectedly contains a UTF-8 BOM")
    text = raw.decode("ascii")
    lines = text.splitlines()
    try:
        header_index = lines.index(QAC_HEADER)
    except ValueError as error:
        raise ValueError("QAC TSV header is missing") from error

    records: list[dict[str, Any]] = []
    malformed: list[int] = []
    blank_after_header: list[int] = []
    for line_number, line in enumerate(lines[header_index + 1 :], header_index + 2):
        if not line:
            blank_after_header.append(line_number)
            continue
        parts = line.split("\t")
        location_match = LOCATION_PATTERN.fullmatch(parts[0]) if parts else None
        if len(parts) != 4 or location_match is None:
            malformed.append(line_number)
            continue
        records.append(
            {
                "line": line_number,
                "location": tuple(int(value) for value in location_match.groups()),
                "form": parts[1],
                "tag": parts[2],
                "features": parts[3],
            }
        )
    if malformed:
        raise ValueError(
            f"QAC candidate has malformed records at lines {malformed[:5]}"
        )
    if blank_after_header:
        raise ValueError("QAC candidate has blank lines in the record region")

    locations = [record["location"] for record in records]
    words = [location[:3] for location in locations]
    verses = [location[:2] for location in locations]
    unique_locations = set(locations)
    unique_words = set(words)
    unique_verses = set(verses)
    tag_counts: collections.Counter[str] = collections.Counter()
    feature_key_counts: collections.Counter[str] = collections.Counter()
    unkeyed_feature_token_counts: collections.Counter[str] = collections.Counter()
    record_kind_counts: collections.Counter[str] = collections.Counter()
    prohibited_feature_hits: list[dict[str, Any]] = []
    empty_form_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    internal_space_forms: list[dict[str, Any]] = []

    for record in records:
        tag_counts[record["tag"]] += 1
        if record["form"] == "":
            empty_form_counts[(record["tag"], record["features"])] += 1
        if any(character.isspace() for character in record["form"]):
            internal_space_forms.append(
                {
                    "line": record["line"],
                    "location": _format_location(record["location"]),
                    "form": record["form"],
                }
            )
        for token in record["features"].split("|"):
            if token in {"PREFIX", "STEM", "SUFFIX"}:
                record_kind_counts[token] += 1
            if ":" in token:
                feature_key_counts[token.split(":", 1)[0]] += 1
            elif token not in {"PREFIX", "STEM", "SUFFIX"}:
                unkeyed_feature_token_counts[token] += 1
            if any(marker in token.upper() for marker in PROHIBITED_FEATURE_MARKERS):
                prohibited_feature_hits.append(
                    {
                        "line": record["line"],
                        "location": _format_location(record["location"]),
                        "token": token,
                    }
                )

    segments_by_word: dict[tuple[int, int, int], list[int]] = collections.defaultdict(
        list
    )
    word_numbers_by_verse: dict[tuple[int, int], set[int]] = collections.defaultdict(
        set
    )
    for surah, ayah, word, segment in locations:
        segments_by_word[(surah, ayah, word)].append(segment)
        word_numbers_by_verse[(surah, ayah)].add(word)

    order_violations = sum(right <= left for left, right in pairwise(locations))
    noncontiguous_segment_words = sum(
        segment_numbers != list(range(1, len(segment_numbers) + 1))
        for segment_numbers in segments_by_word.values()
    )
    noncontiguous_word_verses = sum(
        sorted(word_numbers) != list(range(1, max(word_numbers) + 1))
        for word_numbers in word_numbers_by_verse.values()
    )

    expected_counts = (
        (len(records), EXPECTED_QAC_RECORDS, "record"),
        (len(unique_words), EXPECTED_QAC_WORDS, "word"),
        (len(unique_verses), EXPECTED_QAC_VERSES, "verse"),
        (len({verse[0] for verse in unique_verses}), EXPECTED_QAC_SURAHS, "surah"),
    )
    for actual, expected, label in expected_counts:
        if actual != expected:
            raise ValueError(f"QAC {label} count is {actual}, expected {expected}")

    return {
        "path": path.resolve(),
        "raw": raw,
        "lines": lines,
        "records": records,
        "unique_verses": unique_verses,
        "word_numbers_by_verse": word_numbers_by_verse,
        "physical": {
            "filename": path.name,
            "byte_size": len(raw),
            "sha256": _sha256(raw),
            "container": "uncompressed plain text",
            "encoding": "US-ASCII byte repertoire; strict ASCII and UTF-8 decoding both pass",
            "utf8_bom": False,
            "line_endings": "CRLF",
            "crlf_count": raw.count(b"\r\n"),
            "lf_count": raw.count(b"\n"),
            "bare_cr_count": raw.count(b"\r") - raw.count(b"\r\n"),
            "final_newline": "CRLF",
            "physical_line_count": len(lines),
            "header_line": header_index + 1,
            "comment_lines_before_header": sum(
                line.startswith("#") for line in lines[:header_index]
            ),
            "blank_lines_before_header": sum(not line for line in lines[:header_index]),
        },
        "shape": {
            "columns": QAC_HEADER.split("\t"),
            "record_count": len(records),
            "surah_count": len({verse[0] for verse in unique_verses}),
            "verse_count": len(unique_verses),
            "word_count": len(unique_words),
            "segment_count": len(records),
            "unique_location_count": len(unique_locations),
            "max_segments_per_word": max(
                len(value) for value in segments_by_word.values()
            ),
            "empty_form_count": sum(empty_form_counts.values()),
            "empty_form_classes": [
                {"tag": key[0], "features": key[1], "count": count}
                for key, count in sorted(empty_form_counts.items())
            ],
            "internal_space_form_count": len(internal_space_forms),
            "internal_space_forms": internal_space_forms,
            "empty_tag_count": sum(not record["tag"] for record in records),
            "empty_features_count": sum(not record["features"] for record in records),
            "malformed_record_count": len(malformed),
            "duplicate_location_count": len(records) - len(unique_locations),
            "order_violation_count": order_violations,
            "noncontiguous_segment_word_count": noncontiguous_segment_words,
            "noncontiguous_word_verse_count": noncontiguous_word_verses,
        },
        "tag_counts": dict(sorted(tag_counts.items())),
        "record_kind_counts": dict(sorted(record_kind_counts.items())),
        "feature_key_counts": dict(sorted(feature_key_counts.items())),
        "unkeyed_feature_token_counts": dict(
            sorted(unkeyed_feature_token_counts.items())
        ),
        "prohibited_feature_hits": prohibited_feature_hits,
    }


def _format_location(location: tuple[int, ...]) -> str:
    return "(" + ":".join(str(value) for value in location) + ")"


def _without_combining_marks(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )


def _field_disposition(qac: dict[str, Any]) -> dict[str, Any]:
    matrix = [
        {
            "source_field": "LOCATION",
            "type": "tuple(surah, ayah, word, segment), one-based decimal integers",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Permitted only as a structural locator reconciled to Tanzil verse identity.",
        },
        {
            "source_field": "FORM",
            "type": "Buckwalter-style ASCII segment surface; may be empty or contain an internal space",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "A source surface annotation, not lexical meaning or canonical Quran text.",
        },
        {
            "source_field": "TAG",
            "type": "segment-level tag from the observed 45-value inventory",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "A grammatical category only; PN does not authorize ontology or named-entity meaning.",
        },
        {
            "source_field": "FEATURES.record_kind",
            "type": "PREFIX | STEM | SUFFIX",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Structural segmentation only.",
        },
        {
            "source_field": "FEATURES.POS",
            "type": "POS:<tag> on STEM rows",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Part-of-speech annotation, not semantic class.",
        },
        {
            "source_field": "FEATURES.LEM",
            "type": "LEM:<Buckwalter-style lemma>",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Lemma grouping is structural annotation and cannot establish lexical meaning.",
        },
        {
            "source_field": "FEATURES.ROOT",
            "type": "ROOT:<Buckwalter-style root>",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Root assignment is structural evidence only and cannot establish semantic truth or Root Core.",
        },
        {
            "source_field": "FEATURES.MOOD",
            "type": "MOOD:JUS | MOOD:SUBJ",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Explicit grammatical mood only.",
        },
        {
            "source_field": "FEATURES.PRON",
            "type": "PRON:<person/gender/number code>",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Pronoun morphology only.",
        },
        {
            "source_field": "FEATURES.SP",
            "type": "SP:<upstream code>; observed values <in~, kaAn, kaAd",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Preserve the exact code; Stage C must not infer an undocumented meaning.",
        },
        {
            "source_field": "FEATURES.affix",
            "type": "f:/l:/w:/A: prefix codes, literal affix tokens, and +n:EMPH suffix code",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Segment/affix grammar only.",
        },
        {
            "source_field": "FEATURES.flags",
            "type": "aspect, voice, verb form, person, gender/number, case, definiteness, participle/verbal-noun flags",
            "structural_candidate": True,
            "prohibited_semantic_use": True,
            "reason": "Explicit morphology may be preserved; it cannot be promoted to meaning.",
        },
        {
            "source_field": "SYNTAX_OR_DEPENDENCY",
            "type": "absent from this morphology file",
            "structural_candidate": False,
            "prohibited_semantic_use": True,
            "reason": "The wider QAC project has a treebank, but this candidate artifact supplies no syntax columns or relations.",
        },
        {
            "source_field": "GLOSS_OR_TRANSLATION",
            "type": "absent",
            "structural_candidate": False,
            "prohibited_semantic_use": True,
            "reason": "Prohibited semantic content and not present in the candidate bytes.",
        },
        {
            "source_field": "ONTOLOGY_OR_SEMANTIC_CLASS",
            "type": "absent",
            "structural_candidate": False,
            "prohibited_semantic_use": True,
            "reason": "The separate QAC ontology is outside this artifact and cannot enter through the structural role.",
        },
        {
            "source_field": "LEXICAL_MEANING_OR_INTERPRETIVE_LABEL",
            "type": "absent",
            "structural_candidate": False,
            "prohibited_semantic_use": True,
            "reason": "No lexical-meaning authority is present or permitted.",
        },
        {
            "source_field": "SEMANTIC_RELATION_OR_CONFIDENCE",
            "type": "absent",
            "structural_candidate": False,
            "prohibited_semantic_use": True,
            "reason": "No semantic relation/confidence authority is present or permitted.",
        },
    ]
    return {
        "schema_version": "1.0.0",
        "source_artifact_sha256": qac["physical"]["sha256"],
        "observed_columns": qac["shape"]["columns"],
        "record_kind_counts": qac["record_kind_counts"],
        "tag_counts": qac["tag_counts"],
        "feature_key_counts": qac["feature_key_counts"],
        "unkeyed_feature_token_counts": qac["unkeyed_feature_token_counts"],
        "prohibited_feature_marker_hit_count": len(qac["prohibited_feature_hits"]),
        "field_disposition_matrix": matrix,
    }


def _tanzil_reconciliation(qac: dict[str, Any]) -> dict[str, Any]:
    text_path = (
        REPOSITORY_ROOT / "data" / "corpus" / "tanzil" / "tanzil-uthmani-1.1.txt"
    )
    index_path = (
        REPOSITORY_ROOT / "data" / "corpus" / "tanzil" / "quran-verse-index-v1.0.json"
    )
    text_raw = text_path.read_bytes()
    index_raw = index_path.read_bytes()
    index = json.loads(index_raw.decode("utf-8"))
    text_lines = text_raw.decode("utf-8-sig").splitlines()
    index_entries = [
        (surah["surah"], verse["ayah"], verse["line"])
        for surah in index["surahs"]
        for verse in surah["verses"]
    ]
    index_references = {(surah, ayah) for surah, ayah, _line in index_entries}
    if index_references != qac["unique_verses"]:
        raise ValueError("QAC and active Tanzil verse-reference identity sets differ")

    basmala_words = text_lines[0].split()
    if len(basmala_words) != 4:
        raise ValueError("Active Tanzil basmala token assumption changed")
    raw_mismatches: list[dict[str, Any]] = []
    reconciled_mismatches: list[dict[str, Any]] = []
    basmala_adjustments: list[str] = []
    for surah, ayah, line_number in index_entries:
        reference = (surah, ayah)
        qac_word_count = max(qac["word_numbers_by_verse"][reference])
        tanzil_words = text_lines[line_number - 1].split()
        raw_count = len(tanzil_words)
        if qac_word_count != raw_count:
            raw_mismatches.append(
                {
                    "verse_ref": f"{surah}:{ayah}",
                    "qac_word_count": qac_word_count,
                    "tanzil_whitespace_word_count": raw_count,
                }
            )
        adjusted_words = tanzil_words
        if ayah == 1 and surah not in {1, 9}:
            if [_without_combining_marks(word) for word in tanzil_words[:4]] != [
                _without_combining_marks(word) for word in basmala_words
            ]:
                raise ValueError(f"Expected embedded opening basmala at {surah}:1")
            adjusted_words = tanzil_words[4:]
            basmala_adjustments.append(f"{surah}:1")
        if qac_word_count != len(adjusted_words):
            mismatch_class = (
                "TANZIL_1_1_BA_DA_MA_SPLIT"
                if reference in {(2, 181), (8, 6), (13, 37)}
                else "QAC_INTERNAL_SPACE_COLLAPSES_TWO_TANZIL_WORDS"
                if reference == (37, 130)
                else "UNCLASSIFIED_WORD_COUNT_DIFFERENCE"
            )
            reconciled_mismatches.append(
                {
                    "verse_ref": f"{surah}:{ayah}",
                    "qac_word_count": qac_word_count,
                    "adjusted_tanzil_word_count": len(adjusted_words),
                    "class": mismatch_class,
                }
            )

    expected_residuals = {"2:181", "8:6", "13:37", "37:130"}
    actual_residuals = {item["verse_ref"] for item in reconciled_mismatches}
    if actual_residuals != expected_residuals:
        raise ValueError(
            f"Unexpected reconciled word-count differences: {actual_residuals}"
        )

    return {
        "schema_version": "1.0.0",
        "scope": "read-only identity and whitespace-count diagnostic; not import or surface-alignment proof",
        "qac_source_artifact": {
            "sha256": qac["physical"]["sha256"],
            "embedded_tanzil_version_claim": "Uthmani 1.0.2",
            "verse_reference_grammar": "(surah:ayah:word:segment), one-based",
        },
        "active_tanzil": {
            "source_id": "TANZIL_QURAN_UTHMANI",
            "version": "1.1",
            "text_path": text_path.relative_to(REPOSITORY_ROOT).as_posix(),
            "text_byte_size": len(text_raw),
            "text_sha256": _sha256(text_raw),
            "identity_index_path": index_path.relative_to(REPOSITORY_ROOT).as_posix(),
            "identity_index_byte_size": len(index_raw),
            "identity_index_sha256": _sha256(index_raw),
            "verse_count": len(index_entries),
            "surah_count": len(index["surahs"]),
        },
        "identity_result": {
            "qac_reference_count": len(qac["unique_verses"]),
            "tanzil_reference_count": len(index_references),
            "reference_sets_equal": True,
            "qac_only_reference_count": 0,
            "tanzil_only_reference_count": 0,
        },
        "word_count_diagnostic": {
            "raw_mismatch_verse_count": len(raw_mismatches),
            "embedded_opening_basmala_adjustment_count": len(basmala_adjustments),
            "embedded_opening_basmala_policy": (
                "Active Tanzil 1.1 includes four basmala whitespace tokens at each surah start "
                "except surahs 1 and 9; QAC word locators exclude those added tokens."
            ),
            "residual_mismatch_verse_count": len(reconciled_mismatches),
            "residual_mismatches": reconciled_mismatches,
        },
        "known_non_count_mismatch_classes": [
            {
                "class": "TANZIL_2021_SMALL_YEH_RENDERING_CHANGE",
                "evidence": "https://github.com/kaisdukes/quranic-corpus/issues/52",
                "requirement": "Stage C must use an explicit reviewed transliteration/orthography mapping and must not infer equality from word counts.",
            }
        ],
        "stage_c_requirements": [
            "Treat Tanzil as sole Quran-text and verse-identity authority; never overwrite its text from QAC FORM.",
            "Parse and retain the complete one-based QAC word/segment locator before alignment.",
            "Handle the 112 embedded opening-basmala offsets explicitly and test surahs 1 and 9 as negative boundaries.",
            "Resolve the three ba'da ma word splits and the 37:130 internal-space form through an explicit reviewed exception registry.",
            "Apply a versioned Buckwalter-to-Arabic and orthographic comparison profile; record exact mismatch diagnostics and fail closed on unregistered differences.",
            "Require all 6,236 verse references and every token/segment to align uniquely; missing, duplicate, ambiguous, or text-mismatched records remain outside canonical knowledge.",
        ],
    }


def _requirements_and_gaps(qac: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "source_artifact_sha256": qac["physical"]["sha256"],
        "stage_c_importer_requirements": [
            "Accept the exact uncompressed CRLF ASCII/UTF-8-compatible artifact; hash raw bytes before decoding or newline conversion.",
            "Require the literal TSV header LOCATION, FORM, TAG, FEATURES at physical line 57 after preserving/validating both copyright blocks.",
            "Split records on tabs into exactly four fields; never parse this distribution as pipe-delimited fixture data.",
            "Parse LOCATION with the exact one-based grammar (surah:ayah:word:segment) and preserve segment order and multi-segment words.",
            "Preserve FORM exactly, including 208 intentional empty PRON suffix surfaces and the one internal-space form at (37:130:3:1).",
            "Preserve the top-level TAG and the ordered pipe-delimited FEATURES tokens without inventing meanings for unknown keys or flags.",
            "Recognize PREFIX, STEM, and SUFFIX record kinds; PN is a grammatical proper-name tag, not semantic ontology authority.",
            "Reject wrong hash/size, decoding failure, changed header/notices, wrong column count, malformed locator, noncontiguous indices, duplicate locator, order regression, or unsupported feature vocabulary before persistence.",
            "Reject or quarantine prohibited semantic fields if a different distribution adds gloss, translation, ontology, semantic labels/relations, meaning, or confidence data.",
            "Use deterministic location ordering and stable source-bound annotation identities; an exact retry must be idempotent.",
            "Perform complete Tanzil reconciliation under the separately versioned rules in tanzil-reconciliation.json and fail closed on every unregistered ambiguity.",
        ],
        "stage_b_persistence_gap_analysis": [
            {
                "current_surface": "CorpusSnapshot.structural_source and structural_source_version",
                "gap": "Two descriptive strings cannot bind an independently hashed structural artifact, its license/provenance, parser revision, reconciliation profile, or lifecycle.",
                "minimum_future_capability": "Separate structural-source snapshot/admission identity with source ID/version/hash/size/reference/provenance and immutable verification metadata.",
            },
            {
                "current_surface": "CorpusOccurrence",
                "gap": "Verse-level row has only snapshot_id, expression, verse_ref, and text, with one row per verse; it cannot preserve 128,219 segment annotations.",
                "minimum_future_capability": "Separate annotation table keyed to Tanzil snapshot/occurrence plus word and segment indices, without changing Tanzil text.",
            },
            {
                "current_surface": "No token/segment annotation model or migration",
                "gap": "No columns/constraints exist for source-bound FORM, TAG/POS, lemma, root, record kind, voice, or ordered feature tokens.",
                "minimum_future_capability": "Provenance-bound structural annotation schema with uniqueness, ordering, null/empty-form semantics, and explicit permitted-field constraints.",
            },
            {
                "current_surface": "QACAdapter",
                "gap": "Synthetic pipe parser does not parse the real TSV header/records, strips whitespace, misnames LEM as LEMMA, and has fictional semantic fixture fields.",
                "minimum_future_capability": "Stage-C parser built from the qualified real grammar; no implementation is authorized in Stage A.",
            },
            {
                "current_surface": "CorpusImporter fixture path",
                "gap": "Parsed QAC annotations are discarded while only Tanzil verse text is persisted; fixture-only state cannot prove structural import.",
                "minimum_future_capability": "Transactional, idempotent annotation persistence with full-count and reconciliation validation after Stage B exists.",
            },
            {
                "current_surface": "Pydantic/API schemas",
                "gap": "No structural-source snapshot or token/segment annotation read/write contracts exist.",
                "minimum_future_capability": "Governed API/read models exposing structural evidence and provenance without exposing it as semantic truth.",
            },
            {
                "current_surface": "Alignment/coverage services",
                "gap": "No complete root/lemma/form occurrence coverage service or immutable exception registry exists for active Tanzil 1.1.",
                "minimum_future_capability": "Complete, diagnostics-bearing reconciliation and coverage services with negative-path tests.",
            },
        ],
    }


def _stage_d_prerequisites(qac: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "current_decision": "NOT_APPROVED",
        "decision_owner": "Stage D explicit structural-source admission decision",
        "automatic_approval": False,
        "source_artifact_sha256": qac["physical"]["sha256"],
        "prerequisites": [
            {
                "evidence_stage": "A",
                "requirement": "Authoritative upstream project/version/release identity",
                "evidence_present": True,
                "evidence": "Official QAC download and 0.4 release-notes pages.",
            },
            {
                "evidence_stage": "A",
                "requirement": "Exact candidate byte identity, real format, counts, field disposition, and reproducible independent hash check",
                "evidence_present": True,
                "evidence": "Stage-A manifest plus local bytes and immutable public-mirror byte match.",
            },
            {
                "evidence_stage": "A",
                "requirement": "Direct official acquisition/byte-chain evidence for the candidate artifact",
                "evidence_present": False,
                "blocker": "A read-only GET of the official endpoint exposed only a contact-email POST form and no direct artifact link or checksum. No owner contact email was supplied, so official response bytes were not obtained.",
            },
            {
                "evidence_stage": "A",
                "requirement": "Unambiguous license and redistribution/modification conditions for the combined QAC/Tanzil file",
                "evidence_present": False,
                "blocker": "Official GPLv3, QAC no-change/attribution terms, FAQ non-commercial/research/citation language, the embedded historical Tanzil CC BY-ND 3.0 notice, and Tanzil's current CC BY 3.0/no-change page are not authoritatively reconciled.",
            },
            {
                "evidence_stage": "B",
                "requirement": "Accepted separate structural-source and token/segment persistence design, migrations, constraints, and contracts",
                "evidence_present": False,
                "blocker": "Stage B was not authorized or implemented.",
            },
            {
                "evidence_stage": "C",
                "requirement": "Real-artifact parser/importer with deterministic, idempotent, fail-closed validation",
                "evidence_present": False,
                "blocker": "Stage C was not authorized or implemented; the current parser is fixture-only.",
            },
            {
                "evidence_stage": "C",
                "requirement": "Complete active-Tanzil reconciliation and negative-path evidence for every segment",
                "evidence_present": False,
                "blocker": "Stage A established identity compatibility and mismatch requirements only, not production alignment.",
            },
            {
                "evidence_stage": "C",
                "requirement": "Prohibited semantic-field quarantine/rejection and immutable provenance-binding evidence",
                "evidence_present": False,
                "blocker": "Requires the future real importer and persistence boundary.",
            },
        ],
        "stage_d_rule": "Only after every mandatory prerequisite exists may Stage D explicitly decide APPROVED or NOT_APPROVED; no earlier evidence pre-answers that decision.",
    }


def _manifest(qac: dict[str, Any]) -> dict[str, Any]:
    v7_root = next(
        (parent for parent in qac["path"].parents if parent.name == "V7"), None
    )
    if v7_root is None:
        raise ValueError(
            "The inspected artifact is not under the authorized V7 local source area"
        )
    local_candidate_paths = sorted(
        {
            *v7_root.rglob("quranic-corpus-morphology-0.4.txt"),
            *v7_root.rglob("QAC_STRUCTURAL_NOTES.txt"),
        },
        key=str,
    )
    local_candidates = []
    for candidate_path in local_candidate_paths:
        candidate_raw = candidate_path.read_bytes()
        candidate_sha256 = _sha256(candidate_raw)
        if (
            len(candidate_raw) != EXPECTED_QAC_BYTES
            or candidate_sha256 != EXPECTED_QAC_SHA256
        ):
            raise ValueError(f"Divergent QAC candidate copy: {candidate_path}")
        local_candidates.append(
            {
                "path": str(candidate_path),
                "filename": candidate_path.name,
                "classification": (
                    "HISTORICAL_LISAN_RENAMED_BYTE_DUPLICATE"
                    if candidate_path.name == "QAC_STRUCTURAL_NOTES.txt"
                    else "LOCAL_QAC_NAMED_BYTE_COPY"
                ),
                "byte_size": len(candidate_raw),
                "sha256": candidate_sha256,
                "encoding": "US-ASCII byte repertoire",
                "line_endings": "CRLF",
                "container": "uncompressed plain text",
                "record_count": EXPECTED_QAC_RECORDS,
                "byte_relation_to_primary": "IDENTICAL",
            }
        )
    return {
        "schema_version": "1.0.0",
        "task": "QAC_PROVENANCE_AND_ARTIFACT_QUALIFICATION",
        "stage": "A",
        "evidence_date": "2026-08-27",
        "starting_sha": STARTING_SHA,
        "result": CONTINUATION_RESULT,
        "lineage": {
            "prior_result": "QAC_PROVENANCE_AND_ARTIFACT_QUALIFICATION_BLOCKED",
            "continuation_scope": "Official byte binding and authoritative license clarification only",
        },
        "scope_boundary": {
            "performed": "Stage-A official-binding attempt and license/provenance qualification evidence only",
            "not_performed": [
                "Stage B persistence",
                "Stage C importer",
                "Stage D admission decision",
                "Stage E activation",
                "Purity implementation",
                "semantic root runs",
                "LQE work",
            ],
        },
        "upstream": {
            "project": "Quranic Arabic Corpus",
            "publisher_maintainer": (
                "Copyright holder and release contact Kais Dukes; project initiated at "
                "the University of Leeds; official site footer says maintained by the "
                "quran.com team"
            ),
            "canonical_download": "https://corpus.quran.com/download/default.jsp",
            "release_notes": "https://corpus.quran.com/releasenotes.jsp",
            "release": "morphology version 0.4",
            "release_date": "2011-05-01",
            "candidate_filename": qac["physical"]["filename"],
            "official_acquisition": "Submit a contact email on the official download page and retain the response bytes without text-mode conversion.",
            "official_checksum_published_on_inspected_pages": False,
            "immutable_official_artifact_revision_found_on_inspected_pages": False,
        },
        "official_binding_attempt": {
            "classification": "DIRECT_OFFICIAL_BYTE_BINDING_UNAVAILABLE",
            "attempted_at_utc": OFFICIAL_BINDING_ATTEMPTED_AT_UTC,
            "endpoint": "https://corpus.quran.com/download/default.jsp",
            "request_method": "GET",
            "contact_email_submitted": False,
            "response": {
                "http_status": 200,
                "final_url": "https://corpus.quran.com/download/default.jsp",
                "content_type": "text/html; charset=UTF-8",
                "content_length_bytes": 7272,
                "last_modified": None,
                "server": "cloudflare",
            },
            "form": {
                "method": "POST",
                "action": "/download/default.jsp",
                "contact_email_field": "txtEmail",
                "hidden_fields": ["downloadID", "validEmail"],
            },
            "direct_artifact_link_found": False,
            "official_artifact_obtained": False,
            "official_artifact_filename": None,
            "official_artifact_byte_size": None,
            "official_artifact_sha256": None,
            "comparison_to_candidate": "NOT_COMPUTABLE",
            "reason": "The official page requires submission of a real contact email before delivery. No owner email was supplied or authorized, and no email was fabricated or inferred.",
            "owner_action_required": "Owner submits an authorized contact email through the official form, preserves the delivered response bytes unchanged outside the repository, and provides those bytes for size/SHA-256 comparison.",
        },
        "candidate_artifact": {
            "source_classification": "LOCAL_CANDIDATE_BYTES_NOT_YET_BOUND_AS_UPSTREAM_ARTIFACT",
            "local_path": str(qac["path"]),
            "repository_disposition": "EXTERNAL_READ_ONLY_NOT_COPIED_NOT_COMMITTED",
            **qac["physical"],
            **qac["shape"],
            "header_identity": "Quranic Arabic Corpus (morphology, version 0.4)",
            "header_copyright": "Copyright (C) 2011 Kais Dukes",
            "embedded_text_identity": "Tanzil Quran Text (Uthmani, version 1.0.2)",
            "transformed": False,
        },
        "local_candidate_copies": local_candidates,
        "public_byte_reproduction": {
            "classification": "THIRD_PARTY_IMMUTABLE_MIRROR_CORROBORATION_NOT_UPSTREAM_AUTHORITY",
            "repository": "https://github.com/bnjasim/quranic-corpus",
            "commit": "74416e4881d79e09713c170c7234226cb1785555",
            "raw_url": "https://raw.githubusercontent.com/bnjasim/quranic-corpus/74416e4881d79e09713c170c7234226cb1785555/quranic-corpus-morphology-0.4.txt",
            "observed_http_status": 200,
            "observed_byte_size": EXPECTED_QAC_BYTES,
            "observed_sha256": EXPECTED_QAC_SHA256,
            "observed_etag": '"b154315e0f2eeaa527ad48816b14a84e972f2e88b9b477c5cbceee9417e33eae"',
        },
        "historical_hash_disposition": {
            "lead": EXPECTED_QAC_SHA256,
            "classification": "EXACT_CANDIDATE_ARTIFACT_MATCH + EXACT_PUBLIC_MIRROR_BYTE_MATCH + DIRECT_OFFICIAL_UPSTREAM_BYTE_CHAIN_UNRESOLVED",
        },
        "provenance": {
            "status": "PENDING",
            "established": "Official project, maintainer, version, release date, download location, candidate header identity, and exact public-mirror byte reproduction.",
            "unresolved": "The official endpoint supplied no bytes without owner contact-email submission, and no official checksum or immutable release reference binds its eventual response to the candidate bytes.",
        },
        "license": {
            "status": "PENDING",
            "official_license_page": "https://corpus.quran.com/license.jsp",
            "official_faq": "https://corpus.quran.com/faq.jsp",
            "official_download_terms": "https://corpus.quran.com/download/default.jsp",
            "official_tanzil_text_license": "https://tanzil.net/docs/text_license",
            "candidate_header_claims": [
                "QAC annotation: GNU General Public License; verbatim copying/distribution allowed; changing not allowed; QAC attribution/link and notice retention required.",
                "Embedded Tanzil Uthmani 1.0.2 text: Creative Commons BY-ND 3.0 Unported; verbatim copying/distribution allowed; changing not allowed; Tanzil attribution/link and notice retention required.",
            ],
            "current_tanzil_page_claim": "Creative Commons Attribution 3.0, while separately stating that verbatim copying/distribution is allowed but changing the text is not allowed and attribution/link/notice retention are required.",
            "conflict": "Official GPLv3 modification and commercial-conveyance rights conflict with QAC no-change and FAQ non-commercial/research/citation language. The embedded historical Tanzil CC BY-ND 3.0 notice also differs from Tanzil's current CC BY 3.0 label while both state no change.",
            "local_use": "PENDING_AUTHORITY_CLARIFICATION",
            "raw_redistribution_with_repository_or_application": "NOT_QUALIFIED",
            "public_repository_redistribution": "NOT_QUALIFIED",
            "private_repository_redistribution": "NOT_QUALIFIED",
            "independent_end_user_acquisition": "UNRESOLVED",
            "separate_derived_structural_annotations": "UNRESOLVED; semantic and gloss content remains excluded from the proposed structural role regardless.",
            "raw_repository_commit_permitted": "NOT_QUALIFIED; keep the raw artifact local and uncommitted pending authoritative clarification.",
            "clarification_request": "docs/evidence/qac-stage-a-2026-08-27/QAC_LICENSE_CLARIFICATION_REQUEST.md",
            "request_sent": False,
        },
        "five_axis_final_state": {
            "artifact_identity": "PENDING",
            "provenance_license": "PENDING",
            "structural_role_authorization": "NOT_APPROVED",
            "real_importer": "NOT_IMPLEMENTED",
            "production_activation": "NOT_AUTHORIZED",
            "runtime_source_role": "SOURCE_ROLE_PENDING",
        },
        "blockers": [
            "DIRECT_OFFICIAL_BYTE_BINDING_UNAVAILABLE: the email-gated official endpoint supplied no artifact bytes during the read-only GET attempt.",
            "PROVENANCE_LICENSE=PENDING: authoritative sources do not reconcile GPLv3, QAC no-change, FAQ non-commercial/research/citation, or historical/current Tanzil terms for the requested local-use and redistribution cases.",
        ],
        "exact_owner_action": "Use an owner-authorized contact email in the official download form, preserve and provide the delivered raw bytes, and send the prepared factual clarification request to the official QAC contact. Do not commit or redistribute the raw artifact unless the response clearly qualifies that action.",
    }


def _render_outputs(artifact: Path) -> dict[str, str]:
    qac = _parse_qac(artifact)
    payloads = {
        "artifact-manifest.json": _manifest(qac),
        "field-disposition.json": _field_disposition(qac),
        "requirements-and-gaps.json": _requirements_and_gaps(qac),
        "stage-d-prerequisites.json": _stage_d_prerequisites(qac),
        "tanzil-reconciliation.json": _tanzil_reconciliation(qac),
    }
    return {name: _json_text(payload) for name, payload in payloads.items()}


def _hash_manifest(output: Path, generated_outputs: dict[str, str]) -> str:
    package_files = sorted(
        path
        for path in output.iterdir()
        if path.is_file() and path.name != "artifact-hashes.json"
    )
    expected_generated_names = set(generated_outputs)
    actual_generated_names = {
        path.name for path in package_files if path.suffix == ".json"
    }
    if actual_generated_names != expected_generated_names:
        raise ValueError(
            f"Unexpected generated JSON set: {sorted(actual_generated_names)}; "
            f"expected {sorted(expected_generated_names)}"
        )
    files = {
        path.relative_to(REPOSITORY_ROOT).as_posix(): _sha256(path.read_bytes())
        for path in package_files
    }
    generator_path = Path(__file__).resolve()
    files[generator_path.relative_to(REPOSITORY_ROOT).as_posix()] = _sha256(
        generator_path.read_bytes()
    )
    return _json_text(
        {
            "schema_version": "1.0.0",
            "scope": "Stage-A evidence files plus the generator; excludes this self-referential manifest and the external raw QAC artifact",
            "files": dict(sorted(files.items())),
        }
    )


def _check_or_write(path: Path, expected: str, check: bool) -> None:
    if check:
        if not path.is_file():
            raise ValueError(f"Missing generated evidence file: {path}")
        if path.read_text(encoding="utf-8") != expected:
            raise ValueError(f"Generated evidence drift: {path}")
        return
    path.write_text(expected, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    artifact = args.artifact.resolve()
    output = args.output.resolve()
    if not artifact.is_file():
        raise ValueError(f"QAC artifact does not exist: {artifact}")
    if not output.is_dir():
        raise ValueError(f"Evidence output directory does not exist: {output}")

    generated_outputs = _render_outputs(artifact)
    for name, expected in generated_outputs.items():
        _check_or_write(output / name, expected, args.check)
    hash_manifest = _hash_manifest(output, generated_outputs)
    _check_or_write(output / "artifact-hashes.json", hash_manifest, args.check)
    print(
        "QAC_STAGE_A_EVIDENCE_OK "
        f"mode={'check' if args.check else 'write'} "
        f"artifact_sha256={EXPECTED_QAC_SHA256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
