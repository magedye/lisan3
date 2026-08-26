# Quranic Arabic Corpus Pending Admission Record

Authority revision: `LISAN3_QAC_PENDING_ADMISSION_V3_2026_08_27`

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

## Required lifecycle and dependency sequence

The following stages are ordered prerequisites. Completion of one stage does
not grant the state owned by a later stage.

1. **QAC provenance and artifact qualification:** pin the exact acquisition
   URL, upstream version/release, artifact filename, byte size, file format,
   and SHA-256; verify license and provenance obligations; inventory proposed
   fields, prohibited semantic fields, importer requirements, and structural
   mappings. This qualification is not admission. Structural role
   authorization remains `NOT_APPROVED`, the importer remains
   `NOT_IMPLEMENTED`, and production activation remains `NOT_AUTHORIZED`.
2. **Structural domain and persistence capability:** establish the separate
   provenance-bound token/segment annotation model, identity, constraints, and
   reconciliation boundary required for permitted structural fields. Tanzil
   remains Quran-text and verse-identity authority.
3. **Real QAC importer and validation:** implement and test deterministic
   parsing of the qualified real artifact, complete format and segment
   preservation, prohibited-field rejection, Tanzil reconciliation, immutable
   provenance binding, fail-closed malformed/unsupported input behavior, and
   relevant persistence validation.
4. **QAC structural-source admission decision:** only after the preceding
   evidence exists may governance explicitly decide `APPROVED` or
   `NOT_APPROVED` for the proposed structural role. Qualification, domain, and
   importer evidence never grant approval automatically.
5. **Production activation:** only after an approved structural role, validated
   importer, governed artifact, persistence/reconciliation evidence, and the
   required verification may a separate production-activation transition be
   considered.

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

No QAC artifact may enter canonical knowledge or be activated for production,
and no semantic-pilot run may claim QAC-derived morphology, syntax, root, or
lemma evidence while any of the five axes above remains open. A future,
separately authorized non-production importer-validation exercise against a
qualified artifact is prerequisite evidence, not admission or activation.
