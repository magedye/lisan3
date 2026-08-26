# Tanzil Quranic Text — LISAN3 Admission Record

**authority revision**: `LISAN3_TANZIL_ADMISSION_V1_2026_08_26`
**source_id**: `TANZIL_QURAN_UTHMANI`
**source_name**: Tanzil Quran Text (Uthmani)
**source_role**: Primary Canonical Text Source / `SOURCE_ROLE_APPROVED`
**exact version/release**: Tanzil Uthmani `1.1`
**text profile**: Hafs an Asim, Madinah Mushaf, Uthmani text
**source URL**: `https://tanzil.net/pub/download/`
**download profile**:
`quranType=uthmani&outType=txt&agree=true&alef=true`
**license**: Creative Commons Attribution 3.0; verbatim distribution with
the embedded Tanzil attribution block preserved.

## Authority-bound artifact

- Repository reference:
  `data/corpus/tanzil/tanzil-uthmani-1.1.txt`
- Expected and verified SHA-256:
  `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`
- Expected and verified size: `1,334,737` bytes.
- Format: `TANZIL_UTHMANI_1_1_ONE_VERSE_PER_LINE_UTF8_LF`.
- Encoding/newlines: strict UTF-8, no BOM, LF-only, final LF present.
- Content records: exactly `6,236` non-empty, non-comment verse lines.
- Rights metadata: 28 comment lines and the Tanzil Uthmani 1.1 copyright
  block are preserved verbatim.
- Normalization policy: **none at the canonical text layer**. Import preserves
  each verse line exactly; normalization would change the canonical bytes.

The previous `v1.0.2` value was unverified placeholder metadata and is
superseded by the artifact's embedded version marker, byte verification, and
the provenance evidence below.

## Authority-bound identity mapping

- Repository reference:
  `data/corpus/tanzil/quran-verse-index-v1.0.json`
- SHA-256:
  `0d0a2273e82ebb0d9848ccbf831f1bb297c0fb255413c5aeb299bbfaf2bbc967`
- Role: derived position-only mapping from physical artifact line to
  `surah:ayah`; it contains no Quran text and cannot replace the raw artifact.
- Serialization: the factual mapping was copied from the verified source index
  and mechanically converted from CRLF to repository-standard LF; its LISAN3
  hash therefore binds this local derived serialization.
- Required structure: 114 surahs, canonical per-surah ayah counts, 6,236
  unique identities, deterministic order, and exact source-hash binding.

## Artifact provenance

The repository artifact is a byte-identical copy of:

`D:/APP/tafseer/V7/v7.3.0-candidate/18_CANONICAL_QURAN/raw/tanzil-uthmani-1.1.txt`

That source's acquisition report records a direct HTTP 200 download on
2026-08-20 at 10:47:48 +03:00 using the profile above. LISAN3 independently
recomputed the source and destination byte size and SHA-256 before binding
this record. The external report supports provenance only; its governance
status is not imported into LISAN3.

## Current lifecycle and boundary

```text
SOURCE_ROLE_APPROVED
→ ARTIFACT_PRESENT
→ EXPECTED_HASH_BOUND
→ HASH_VERIFIED
→ import validation pending until persisted service evidence passes
→ CANONICAL_ACTIVATION_PENDING
```

Allowed fields are Surah, Ayah, and exact Quran text. Translation, tafsir,
gloss, and external semantic fields are forbidden.

External CANON-001 reconciliation is factual only: the source name, version,
artifact size, verse count, and SHA-256 match. After successful LISAN3 import
validation the evidence record may state
`CANON_001_ARTIFACT_IDENTITY_MATCH_CONFIRMED`; it must not import external
adoption or activation status.

`PRODUCTION_ACTIVATION_NOT_GRANTED`
**decision rationale**: Provides deterministic, static, heavily verified Uthmani text without injecting semantic bias, suitable for the Blind Lab corpus.
