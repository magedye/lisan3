# Quranic Arabic Corpus (QAC) Morphology — LISAN3 Admission Record

**authority revision**: `LISAN3_QAC_STRUCTURAL_ADMISSION_V1_2026_09_06`
**decision**: `QUALIFIED_QURANIC_MORPHOLOGY_ADMITTED` — admitted as a **local,
hash-bound, acquire-per-install immutable structural source** for root/morphology
annotation only. Supersedes the prior `PENDING_ADMISSION` record for the
structural role; the Stage-A evidence remains the byte/format/field basis.

## Source identity (§1, §2, §14)

| Item | Value |
|---|---|
| Source ID | `QAC_MORPHOLOGY` |
| Source name | Quranic Arabic Corpus — Morphology |
| Version / release | `0.4` (release notes dated 2011-05-01) |
| Copyright holder | Kais Dukes (project initiated at the University of Leeds) |
| Filename | `quranic-corpus-morphology-0.4.txt` |
| Byte size | `6,309,503` |
| **SHA-256** | `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46` |
| Container / encoding | uncompressed plain text; strict US-ASCII; no BOM; CRLF |
| Embedded text notice | Tanzil Quran Text, Uthmani 1.0.2 (CC BY-ND 3.0) |
| Local path (gitignored) | `data/corpus/qac/quranic-corpus-morphology-0.4.txt` |

## Acquisition provenance (§3)

- Official canonical location: <http://corpus.quran.com/download> — the official
  download is an email-gated POST form with no direct artifact link or published
  checksum, i.e. a step unavailable to the runtime.
- Bytes acquired from an **immutable-commit-pinned public mirror** whose content is
  **byte-identical** to the documented official artifact:
  `https://raw.githubusercontent.com/bnjasim/quranic-corpus/74416e4881d79e09713c170c7234226cb1785555/quranic-corpus-morphology-0.4.txt`
- Identity established by exact SHA-256 + byte-size match to the Stage-A official
  candidate identity (`docs/evidence/qac-stage-a-2026-08-27/`). Per §3, matching
  the documented artifact hash establishes file identity; the mirror is a
  transport, not an authority.
- Acquisition timestamp: 2026-09-06 (this session).

## License / terms disposition (§2)

Embedded copyright block (read verbatim from the artifact):

- QAC morphology: **GNU General Public License**, © 2011 Kais Dukes. Verbatim
  copies may be distributed; **changing the file is not allowed**; use requires
  clearly indicating the source (Quranic Arabic Corpus) and a link to
  <http://corpus.quran.com>; the copyright notice must be retained in verbatim
  copies and reproduced in derived works containing a substantial portion.
- Embedded Tanzil 1.0.2: CC BY-ND 3.0 (verbatim, no change, attribution/link).

**Disposition:** to avoid an unresolved redistribution/copyleft question and honor
"do not fabricate legal clearance", the raw GPL artifact is **NOT committed** to
this repository. It is admitted for **local structural use, acquire-per-install**:
each installation obtains its own byte-identical copy (mirror/official) and the
importer fail-closes on any SHA drift. Derived structural annotations carry the
required attribution and lineage to the source SHA. Required attribution string:
`Quranic Arabic Corpus (Kais Dukes, 2011), http://corpus.quran.com`.

## Canonical Quran mapping (§5)

- Tanzil (`TANZIL_QURAN_UTHMANI` 1.1) remains the **sole** Quran-text and
  verse-identity authority. QAC is structural annotation over the text; QAC `FORM`
  never overwrites Tanzil text.
- All 6,236 QAC verse references match the admitted Tanzil verse identities
  exactly (0 unmatched). The importer fails closed if any QAC verse is absent.
- Known word-index offsets are recorded, not silently resolved: 112 embedded
  opening-basmala verses (QAC excludes those tokens), and 4 residual cases
  (`2:181`, `8:6`, `13:37` ba'da-ma splits; `37:130` internal-space form). QAC
  word indices are QAC-native; verse identity is Tanzil-authoritative.

## Structural capabilities qualified (§4)

TSV `LOCATION FORM TAG FEATURES`; 128,219 segments (PREFIX 28,670 / STEM 77,915 /
SUFFIX 21,634); `ROOT` on 49,968 segments (Buckwalter, kept as the stable key);
`LEM` on 74,608; `POS`, derived verb form `(I..XII)`, `TAG` (45 categories),
mood/pronoun/affix/flags. **Zero** gloss / ontology / semantic-class / syntax
fields (prohibited-marker hit count 0) — a pure morphological source.

## Derived artifacts (lineage)

- `structural_tokens` rows (runtime, source_id=`QAC_MORPHOLOGY`,
  source_version=`0.4`, extraction_version=`qac-0.4-import-v1`), one per
  root-bearing segment (49,968).
- **Root Universe**: 1,642 roots, deterministically derived and reproducible.

## Reproduction

Acquire the artifact to `data/corpus/qac/quranic-corpus-morphology-0.4.txt`
(SHA-256 above), then the importer `QacMorphologyImporter.import_tokens` verifies
bytes, parses, reconciles with Tanzil, and persists tokens. Qualification tests:
`tests/test_qac_morphology.py` (parse logic always; full-corpus test runs when the
local artifact is present).
