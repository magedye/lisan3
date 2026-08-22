# Quranic Arabic Corpus (QAC) - Admission Record

**source_id**: `QAC_MORPHOLOGY_SYNTAX`
**source_name**: Quranic Arabic Corpus
**source_role**: Auxiliary Structural Source
**exact version/release**: v0.4 (metadata assumed verified locally)
**retrieval/source location**: `https://corpus.quran.com/download/`
**retrieval date if applicable**: Pending local verification
**license/usage/attribution constraints**: GNU GPL
**Current Local Environment Recommendation**: `SOURCE_ROLE_APPROVED`, `ARTIFACT_VERIFICATION_PENDING`, `CANONICAL_ACTIVATION_PENDING`

(Note: Offline datasets cannot be reliably verified or hashed in the current isolated agent context. Production Canonical Activation is pending actual artifact acquisition and verification. The provided implementation boundary uses isolated test fixtures to enforce quarantine mechanics.)
**raw artifact hash**: `ADMISSION_PENDING_ARTIFACT_VERIFICATION` (Awaiting exact local artifact file hash)
**normalization policy**: Mapped to Lisan structural tokens.
**canonical identity mapping**: `CorpusSnapshot` -> `structural_source`
**allowed fields**: Token identity, root, lemma, POS, morphology/features, syntactic dependency.
**forbidden fields**: Semantic Ontology, Semantic tags.
**validation evidence**: `ADMISSION_PENDING_ARTIFACT_VERIFICATION`
**known limitations**: Syntactic dependencies are interpretations and may carry implicit biases. Ontology is strictly forbidden.
**admission decision**: `ADMIT_AS_AUXILIARY_STRUCTURAL_SOURCE`
**decision rationale**: Highly structured morphological and syntactic analysis is essential for structural observations. The semantic ontology is quarantined as it represents external unverified semantic assertions violating Blind Lab rules.
