# QAC Stage-A Provenance and Artifact Qualification

Task: `QAC_PROVENANCE_AND_ARTIFACT_QUALIFICATION`
Starting candidate: `d69d1cadc9c13ccf542b4ebc25e358f7a7846052`
Evidence date: `2026-08-27`
Prior result: `QAC_PROVENANCE_AND_ARTIFACT_QUALIFICATION_BLOCKED`
Result: `QAC_STAGE_A_OFFICIAL_BINDING_AND_LICENSE_BLOCKED`

## Scope and verdict

This package is Stage A evidence only. It does not implement structural
persistence or an importer, decide source admission, activate QAC, implement a
Purity evaluator, run semantic roots, or touch LQE.

A concrete QAC morphology 0.4 candidate exists and its byte identity, format,
counts, fields, and compatibility risks are reproducible. The combined
provenance/license axis remains `PENDING`, however, for two fail-closed reasons:

1. a read-only GET of the official endpoint exposed only a contact-email POST
   form, no direct artifact link, and no published checksum or immutable
   artifact revision. No owner contact email was supplied or fabricated, so no
   official response bytes were obtained;
2. official pages and candidate notices leave GPLv3, QAC no-change,
   FAQ non-commercial/research/citation, embedded historical Tanzil CC BY-ND
   3.0, and current Tanzil CC BY 3.0/no-change statements unresolved.

Consequently, the raw artifact remains external, read-only, and uncommitted.
No authority-bound QAC expected hash is created in runtime.

## Upstream source identity

| Item | Evidence-backed result |
|---|---|
| Project | Quranic Arabic Corpus |
| Publisher/maintainer | Copyright holder and release contact Kais Dukes; project initiated at the University of Leeds; official site footer says maintained by the quran.com team |
| Canonical location | <https://corpus.quran.com/download/default.jsp> |
| Release | Morphological data, version `0.4` |
| Release identity | Release notes dated `2011-05-01`: <https://corpus.quran.com/releasenotes.jsp> |
| Candidate filename | `quranic-corpus-morphology-0.4.txt` |
| Candidate header | QAC morphology version 0.4, Copyright 2011 Kais Dukes |
| Embedded text header | Tanzil Quran Text, Uthmani version 1.0.2 |
| Official acquisition | Enter a contact email on the canonical download page, retain the exact response bytes, then hash before decoding or newline conversion |
| Official immutable reference/checksum | None published on the download or release-notes pages |

## Direct official byte-binding attempt

At `2026-08-26T23:50:10.7789646Z`, a read-only HTTP GET was made to the
canonical download endpoint. The result was HTTP 200 HTML (`text/html;
charset=UTF-8`, 7,272 response bytes), not an artifact response. The page
contained a POST form targeting `/download/default.jsp` with the contact-email
field `txtEmail` and hidden fields `downloadID` and `validEmail`. No direct
`.txt`, archive, or other artifact link was present.

No POST was made because the form requires a real owner contact email and none
was supplied or authorized. No email was fabricated or inferred. Therefore:

- official byte-binding result: `DIRECT_OFFICIAL_BYTE_BINDING_UNAVAILABLE`;
- official artifact filename: `NOT_OBTAINED`;
- official artifact byte size: `NOT_OBTAINED`;
- official artifact SHA-256: `NOT_COMPUTABLE`;
- comparison with the candidate: `NOT_COMPUTABLE`.

The owner action required to perform the comparison is to submit an authorized
contact email through the official form, preserve the delivered raw response
bytes unchanged outside this repository, and provide those bytes for byte-size
and SHA-256 computation. The public mirror remains corroboration only and was
not substituted for direct official evidence.

The official release notes describe morphology segmentation and a separate,
partially complete syntax treebank. The inspected morphology file itself has no
syntax/dependency column. Wider-project capabilities are not silently assigned
to this artifact.

## Candidate provenance and byte reproduction

Primary inspected path:

`D:\APP\tafseer\V7\v7.3.0-candidate\مهارة لسان القرآن\assets\quran\qac\quranic-corpus-morphology-0.4.txt`

Classification:
`LOCAL_CANDIDATE_BYTES_NOT_YET_BOUND_AS_UPSTREAM_ARTIFACT`.

The authorized V7 local area contains thirteen byte-identical copies: seven
under the upstream-style filename and six renamed
`QAC_STRUCTURAL_NOTES.txt`. Every copy is 6,309,503 bytes and has the same
SHA-256. The renamed copies are
`HISTORICAL_LISAN_RENAMED_BYTE_DUPLICATE`, not a different upstream artifact
and not a transformed export. Archive and review-copy locations provide byte
corroboration only; they provide no LISAN3 authority. The exact paths and hashes
are in `artifact-manifest.json`.

The read-only external historical workspace
`D:\APP\tafseer\مواصفات وشكل الجذر النهائي` contained provenance leads and
reports but no physical 6,309,503-byte QAC file. No rejected R2 material was
used as governing evidence, and no historical semantic conclusion was
consumed.

The same bytes were fetched in memory from a third-party GitHub mirror at the
immutable commit `74416e4881d79e09713c170c7234226cb1785555`:

<https://raw.githubusercontent.com/bnjasim/quranic-corpus/74416e4881d79e09713c170c7234226cb1785555/quranic-corpus-morphology-0.4.txt>

The response was HTTP 200, 6,309,503 bytes, and SHA-256
`a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`.
This is independent public byte reproduction, not upstream authority.

## License and redistribution disposition

Official sources inspected:

- download terms: <https://corpus.quran.com/download/default.jsp>;
- linked GNU license: <https://corpus.quran.com/license.jsp>;
- FAQ usage statements: <https://corpus.quran.com/faq.jsp>;
- current Tanzil text license: <https://tanzil.net/docs/text_license>.

The evidence is not internally clean enough to mark the license axis verified:

- the download page labels QAC as GNU GPL and links to GPL version 3;
- the QAC file notice permits verbatim distribution with QAC attribution, a
  link, and notice retention, but says the file must not be changed;
- the embedded historical Tanzil notice labels its Uthmani 1.0.2 text CC BY-ND
  3.0 and also requires verbatim preservation, attribution/linking, and notice
  retention;
- Tanzil's current official page labels its text CC BY 3.0, yet separately says
  the text cannot be changed and repeats attribution/link/notice obligations;
- the FAQ adds non-commercial research-only and publication-citation
  conditions, despite also naming the GNU public license;
- GPLv3 describes modification and commercial-conveyance rights, so the
  no-change and non-commercial language requires authoritative reconciliation.

`PROVENANCE_LICENSE=PENDING`. Unmodified local use has not been finally
qualified against the conflicting authoritative statements. Raw redistribution
with an application or repository is `NOT_QUALIFIED`, for both public and
private repositories. Whether each installation must acquire its own copy is
`UNRESOLVED`. The license treatment of separately derived structural
annotations is also `UNRESOLVED`; semantic and gloss content remains excluded
from the proposed structural role regardless.

Current raw-artifact disposition is
`EXTERNAL_READ_ONLY_NOT_COPIED_NOT_COMMITTED`. Any future normalized or
transformed output would be a separate artifact requiring its own hash,
provenance, notices, and authoritative license qualification.

A factual request covering the exact outstanding cases is prepared at
`QAC_LICENSE_CLARIFICATION_REQUEST.md`. It has status `PREPARED_NOT_SENT`; this
task did not contact any person or service.

## Physical artifact identity

| Property | Exact result |
|---|---|
| Filename | `quranic-corpus-morphology-0.4.txt` |
| Bytes | `6,309,503` |
| SHA-256 | `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46` |
| Container | Uncompressed plain text |
| Encoding | US-ASCII byte repertoire; strict ASCII and UTF-8 both decode |
| BOM | None |
| Line endings | 128,276 CRLF terminators; no bare CR; final CRLF present |
| Physical lines | 128,276 |
| Header | Line 57, exact TSV fields `LOCATION FORM TAG FEATURES` |
| Data records | 128,219 |
| Coverage | 114 surahs, 6,236 verses, 77,429 words, 128,219 segments |

The historical `a1d129...` lead remains classified:

`EXACT_CANDIDATE_ARTIFACT_MATCH + EXACT_PUBLIC_MIRROR_BYTE_MATCH + DIRECT_OFFICIAL_UPSTREAM_BYTE_CHAIN_UNRESOLVED`.

It is not an authority-bound runtime hash.

## Real format and structural inventory

Each data row is TSV with exactly four physical fields:

`LOCATION<TAB>FORM<TAB>TAG<TAB>FEATURES<CRLF>`

- `LOCATION` is `(surah:ayah:word:segment)`, with one-based decimal indices.
  Words contain one to five ordered segments.
- `FORM` is a Buckwalter-style ASCII segment surface. It is not canonical Quran
  text. Exactly 208 `SUFFIX|PRON:1S` segments intentionally have an empty FORM.
  One proper-name FORM, `(37:130:3:1)`, contains an internal ASCII space.
- `TAG` contains 45 observed segment categories. `PN` occurs 3,911 times and is
  a grammatical proper-name category, not semantic-ontology authority.
- `FEATURES` is an ordered pipe-delimited token sequence within the fourth TSV
  field. Record kinds are `PREFIX` (28,670), `STEM` (77,915), and `SUFFIX`
  (21,634). Observed keyed families are `POS`, `LEM`, `ROOT`, `MOOD`, `PRON`,
  `SP`, `f`, `l`, `w`, `A`, and `+n`. Unkeyed tokens include literal affixes
  plus flags for aspect, voice, derived verb form, person, gender/number, case,
  definiteness, participle, and verbal noun.
- `ROOT` occurs on 49,968 segments and `LEM` on 74,608 segments. They are source
  annotations only; neither is semantic truth or Root Core evidence by itself.
- The file has no gloss, translation, ontology, semantic class, lexical
  meaning, interpretive label, semantic relation, confidence, syntax, or
  dependency field. No record has an empty `TAG` or `FEATURES` field.

Integrity diagnostics found zero malformed rows, duplicate locations, ordering
  violations, noncontiguous segment sequences, or noncontiguous word sequences.
The exact 45-tag and feature inventories are in `field-disposition.json`.

## Field disposition matrix

| SOURCE_FIELD | TYPE | STRUCTURAL_CANDIDATE | PROHIBITED_SEMANTIC_USE | REASON |
|---|---|---:|---:|---|
| `LOCATION` | one-based surah/ayah/word/segment tuple | yes | yes | Structural locator only; Tanzil owns verse identity. |
| `FORM` | Buckwalter-style segment surface | yes | yes | Not canonical text and not lexical meaning. |
| `TAG` / `FEATURES.POS` | grammatical category | yes | yes | POS and `PN` cannot become semantic class/ontology. |
| `FEATURES.PREFIX/STEM/SUFFIX` | segment kind | yes | yes | Segmentation only. |
| `FEATURES.LEM` | source lemma annotation | yes | yes | Cannot establish lexical meaning. |
| `FEATURES.ROOT` | source root annotation | yes | yes | Cannot establish semantic truth or Root Core. |
| `FEATURES.MOOD/PRON/SP/affix/flags` | explicit morphology codes | yes, after field review | yes | Preserve exact codes; do not infer undocumented meaning. |
| syntax/dependency | absent | no evidence in this artifact | yes | A separate artifact would require separate qualification. |
| gloss/translation | absent | no | yes | Prohibited semantic content. |
| ontology/semantic class | absent | no | yes | Separate QAC ontology is outside the structural role. |
| lexical meaning/interpretive label | absent | no | yes | No semantic authority. |
| semantic relation/confidence | absent | no | yes | No semantic authority. |

Classification does not delete or normalize any source field. The raw candidate
bytes remain unchanged outside LISAN3.

## Stage-C real importer requirements

Stage C is not implemented here. Its minimum requirements, derived from the
real bytes, are:

1. hash raw bytes before decoding or newline conversion and require the
   qualified size/hash/notices;
2. parse the literal line-57 TSV header and exactly four tab-separated fields;
3. preserve ordered pipe tokens inside `FEATURES`; do not use the current
   synthetic pipe-delimited fixture grammar;
4. preserve one-based location indices, segment order, multi-segment words,
   intentional empty FORM values, and the 37:130 internal-space FORM;
5. preserve top-level `TAG`, record kind, exact keyed codes, and flags without
   undocumented inference;
6. treat `PN` as morphology, not ontology;
7. fail closed on changed bytes/notices, decode/header/column errors, malformed
   locators, noncontiguous indices, duplicates, ordering errors, unknown
   vocabulary, or prohibited semantic additions;
8. generate stable source-bound annotation identities and make exact retry
   idempotent;
9. reconcile every record to the active Tanzil snapshot under a versioned,
   diagnostics-bearing mapping; and
10. persist nothing until Stage B supplies the accepted separate domain.

The current `QACAdapter` strips each line, expects pipe-delimited rows, names a
nonexistent `LEMMA` feature, and tests fictional semantic fields. The current
fixture importer discards parsed structural annotations. Neither is evidence
for this format.

## Tanzil reconciliation requirements

The read-only diagnostic compared QAC locators with the active
`TANZIL_QURAN_UTHMANI` 1.1 identity index and text artifact.

- All 6,236 QAC verse references exactly match the 6,236 active Tanzil verse
  identities; no reference exists on only one side.
- Raw whitespace word counts differ in 116 verses. Of those, 112 are the
  explicit opening-basmala policy: active Tanzil 1.1 embeds four basmala tokens
  at each surah start except surahs 1 and 9, while QAC locators exclude them.
- Four residual word-count differences remain after that adjustment:
  `2:181`, `8:6`, and `13:37` split `ba'da ma` into two Tanzil 1.1 words but one
  QAC word; `37:130` uses two Tanzil whitespace words where QAC stores one FORM
  containing an internal space.
- QAC declares embedded Tanzil Uthmani 1.0.2; active LISAN3 uses Tanzil 1.1.
  A maintainer issue also documents a 2021 small-yeh rendering change and the
  three `ba'da ma` splits:
  <https://github.com/kaisdukes/quranic-corpus/issues/52>.

Word-count agreement is not surface alignment. Stage C must keep Tanzil as sole
text/verse authority, apply a reviewed and versioned Buckwalter/orthography
comparison profile, encode basmala and four residual exceptions explicitly,
and fail closed on every missing, duplicate, ambiguous, or unregistered
text-mismatch case. QAC FORM must never overwrite Tanzil text.

## Stage-B persistence gap analysis

Stage B is not implemented here. Current gaps are:

- `CorpusSnapshot.structural_source*` are two descriptive strings, not an
  independently hashed structural-source snapshot with provenance, license,
  parser revision, and reconciliation identity.
- `CorpusOccurrence` is verse-level and has only snapshot, expression,
  verse-reference, and text fields; its uniqueness is one row per snapshot and
  verse. It cannot hold 128,219 segment annotations.
- no token/segment annotation model, migration, constraints, or lifecycle
  exists for source-bound FORM, TAG/POS, lemma, root, record kind, voice, or
  ordered features;
- no API/read contract exposes separate structural evidence and provenance;
- no immutable active-Tanzil exception registry, complete alignment service, or
  root/lemma/form coverage service exists; and
- the fixture importer discards QAC structure rather than persisting it.

The minimum future envelope is a separate annotation source/snapshot identity
plus records keyed by active Tanzil snapshot/occurrence, verse reference, word
index, and segment index, carrying source ID/version/hash, FORM, root, lemma,
POS, record kind, voice/features, and only separately permitted syntax. Exact
gaps are machine-readable in `requirements-and-gaps.json`.

## Eventual Stage-D prerequisite checklist

Stage D remains an explicit future `APPROVED` or `NOT_APPROVED` decision. It is
not pre-answered by this package.

- **Stage A:** upstream project/version/release identity and candidate
  byte/format/field evidence exist; direct official byte-chain and unambiguous
  license evidence do not exist.
- **Stage B:** an accepted separate structural persistence design, migrations,
  constraints, lifecycle, and contracts must exist; none exists now.
- **Stage C:** a real deterministic importer, complete active-Tanzil
  reconciliation, immutable provenance binding, prohibited-field quarantine,
  idempotency, full-count validation, and negative-path evidence must exist;
  none exists now.

Only after every mandatory prerequisite is present may Stage D decide. See
`stage-d-prerequisites.json`.

## Five-axis final state

| Axis | State after Stage A |
|---|---|
| Artifact identity | `PENDING` — candidate byte identity is established, but official upstream byte binding is not |
| Provenance/license | `PENDING` |
| Structural role authorization | `NOT_APPROVED` |
| Real importer | `NOT_IMPLEMENTED` |
| Production activation | `NOT_AUTHORIZED` |
| Runtime source role | `SOURCE_ROLE_PENDING` |

No runtime authority record, database, production snapshot, sealed pilot
evidence, semantic result, or external LQE workspace was changed.

## Reproduction and verification

After obtaining the exact candidate bytes, run from the LISAN3 repository:

```powershell
.\.venv\Scripts\python.exe tools\qac_stage_a_evidence.py `
  --artifact 'D:\APP\tafseer\V7\v7.3.0-candidate\مهارة لسان القرآن\assets\quran\qac\quranic-corpus-morphology-0.4.txt' `
  --check
```

The checker recomputes the raw SHA-256, physical profile, complete structural
inventory, active-Tanzil diagnostic, generated JSON, and package hashes. It
does not access a database or network and does not import QAC.

## Exact next action

The owner submits an authorized contact email through the official QAC download
form, preserves and provides the delivered raw bytes, and sends the prepared
factual clarification request to the official QAC contact. Then recompute the
official byte size/SHA-256 and compare with the candidate, and record the
authoritative response without broadening Stage A. Do not commit or
redistribute the raw artifact unless the response clearly qualifies that
action. Do not authorize or start Stage B, C, D, or E under this
blocker-resolution action.
