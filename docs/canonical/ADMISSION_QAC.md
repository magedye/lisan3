# Quranic Arabic Corpus Pending Admission Record

Authority revision: `LISAN3_QAC_PENDING_ADMISSION_V2_2026_08_26`

## Source identity

- Source ID: `QAC_MORPHOLOGY_SYNTAX`
- Source name: Quranic Arabic Corpus
- Candidate upstream location: <https://corpus.quran.com/download/>
- Current admission decision: `PENDING_ADMISSION`
- Machine-readable source-role state: `SOURCE_ROLE_PENDING`

This record supersedes the earlier unverified approval claim. It does not admit
an artifact, authorize a source role, prove an importer, activate production
use, or authorize semantic-pilot execution.

## Five-axis admission state

| Axis | State | Current evidence |
|---|---|---|
| Artifact identity | `PENDING` | No exact repository artifact, release identity, byte identity, or expected SHA-256 is recorded. |
| Provenance and license | `PENDING` | The upstream URL is known. The prior GNU GPL claim and exact attribution obligations have not been verified against a pinned artifact. |
| Structural role authorization | `NOT_APPROVED` | QAC is only a proposed auxiliary structural source. No canonical admission decision has approved its role. |
| Real importer | `NOT_IMPLEMENTED` | A synthetic pipe-delimited fixture parser exists. It is not evidence of a parser for an admitted QAC distribution, and current fixture import discards structural annotations. |
| Production activation | `NOT_AUTHORIZED` | No admitted artifact or role exists. `CANONICAL_ACTIVATION_PENDING` is fail-closed runtime storage, not an activation decision. |

## Evidence required before admission can close

1. Pin the exact acquisition URL, upstream version/release, artifact filename,
   byte size, file format, and SHA-256.
2. Verify license, attribution, redistribution, and modification obligations for
   that exact artifact.
3. Review each proposed field against the structural-only role below.
4. Implement and test a real-format importer that preserves source lineage and
   reconciles every annotation to an admitted Tanzil snapshot without changing
   Tanzil text or verse identity.
5. Record a separate explicit source-role admission decision. Artifact and
   importer evidence do not grant that decision automatically.

## Maximum proposed future role

If separately admitted, QAC may contribute only an auxiliary annotation layer
for fields that pass field-by-field review, such as:

- token and segment locators;
- root and lemma annotations;
- part of speech, morphological form, voice, and explicit morphological
  features;
- explicitly permitted syntactic relations.

Tanzil remains the sole canonical authority for Quranic text and verse identity.
QAC annotations must never mutate or silently replace Tanzil content.

The following are prohibited from admission through this structural role:

- glosses and translations;
- ontologies or semantic labels;
- dictionary, tafsir, or derived Root Core content;
- confidence claims or research conclusions;
- any field whose meaning, provenance, or authority remains unresolved.

## Future reconciliation identity

Any future imported annotation must bind to:

`Tanzil snapshot + verse_ref + word index + segment index + QAC source identity`

Multi-segment words must remain multi-segment. Missing, duplicate, or ambiguous
alignment must fail closed and remain outside canonical knowledge.

## Current consequence

No QAC artifact may be imported or activated, and no semantic-pilot run may
claim QAC-derived morphology, syntax, root, or lemma evidence while any of the
five axes above remains open.
