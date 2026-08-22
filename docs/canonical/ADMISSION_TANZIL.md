# Tanzil Quranic Text - Admission Record

**source_id**: `TANZIL_QURAN_UTHMANI`
**source_name**: Tanzil Quran Text (Uthmani)
**source_role**: Primary Canonical Text Source
**exact version/release**: v1.0.2 (metadata assumed verified locally)
**retrieval/source location**: `https://tanzil.net/download/`
**retrieval date if applicable**: Pending local verification
**license/usage/attribution constraints**: Free for non-commercial/academic use, requires attribution.
**Current Local Environment Recommendation**: `SOURCE_ROLE_APPROVED`, `ARTIFACT_VERIFICATION_PENDING`, `CANONICAL_ACTIVATION_PENDING`

(Note: Offline datasets cannot be reliably verified or hashed in the current isolated agent context. Production Canonical Activation is pending actual artifact acquisition and verification. The provided implementation boundary uses isolated test fixtures to enforce parsing logic.)
**canonical identity mapping**: `CorpusSnapshot` -> `canonical_text_source`
**allowed fields**: Surah, Ayah, Text
**forbidden fields**: Any translations or external tafseer commentary.
**validation evidence**: `ADMISSION_PENDING_ARTIFACT_VERIFICATION`
**known limitations**: Requires careful orthographic handling (e.g., Alif Khanjareeya).
**decision rationale**: Provides deterministic, static, heavily verified Uthmani text without injecting semantic bias, suitable for the Blind Lab corpus.
