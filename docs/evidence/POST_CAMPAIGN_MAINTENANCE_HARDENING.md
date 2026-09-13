# Post-campaign maintenance and governance hardening

Date: 2026-09-14
Scope: post-campaign maintenance only; no semantic re-analysis or lifecycle
advancement of ESw, dnw, flH, fwh, or glm.

## Frozen boundary

The five-root campaign is closed. This maintenance scope must not create or
replace a ResearchRun, ObservationArtifact, SemanticClaim, VerificationRecord,
or canonicalization result for the five production roots. It must not modify
Batch 07 artifacts or start Batch 08. The governed database and the five
Batch 07 artifact hashes are rechecked separately as immutable baseline
evidence before and after this work.

## Debt classification

| Track | Classification | Resolution |
| --- | --- | --- |
| A — isolation attestation corroboration | `FIX_NOW` | Canonicalization now corroborates the persisted manifest, actor, timestamp, audit reference, run, snapshot, and methodology binding. |
| B — Research Judgment isolation rule | `NO_DEFECT / DOCUMENT_ONLY` | Research Judgment remains eligible with a clean initialized boundary; requiring `ESTABLISHED` there would create the prohibited research Lock/Purity gate. Canonicalization remains stricter. |
| C — duplicate Alembic entrypoint | `FIX_NOW` | The executable `backend/alembic.ini` is removed; legacy migration history remains in place with a retired notice. |
| D — flH form-only observations | `DEFER` | Filling semantic fields would require new Quran-internal research judgment and could change evidence/claim state. No current row is edited. |
| E — fwh sampling diagnostic | `NO_DEFECT / DOCUMENT_ONLY` | `sampling_basis_recorded=false` is informative for this `UNIVERSAL` exact-set claim, not a coverage failure. No historical claim is rewritten. |
| F — lexical extraction-version selection | `DEFER` | The current rule is consistent but lexicographic. A replacement needs an explicit canonical active-extraction-version authority; inventing one here could affect semantic selection. |
| G — convergence side-store protection | `FIX_NOW` | CLI convergence accepts only the resolved canonical `lisanapp.db` identity; a side store, renamed copy, wrong path, or arbitrary override is refused. |
| H — UTC deprecations | `FIX_NOW` | `utcnow()` defaults are replaced with an explicit UTC-now helper that preserves existing naive `DateTime` storage compatibility. |
| I — historical lifecycle wording | `DOCUMENT_ONLY` | Historical evidence remains byte-stable. The current clear alias is `FIVE_ROOT_CAMPAIGN_COMPLETE_NO_CANONICAL_ADOPTIONS`. |
| J — reopening policy | `DOCUMENT_ONLY` | Future re-opening is constrained below; no claim is reopened by this document. |

## Isolation and research-judgment boundary

`CLEAN` plus `ESTABLISHED` is not enough for canonicalization unless the
attestation itself still resolves and binds the exact run, corpus snapshot,
methodology revision, actor, timestamp, nonempty input manifest, and immutable
`ESTABLISH_SOURCE_ISOLATION` audit event. This is a fail-closed
canonicalization guard only. The Research Judgment path is deliberately not
changed: adding an `ESTABLISHED` requirement there would introduce an
administrative research Lock/Purity gate that canonical authority excludes.

## Existing semantic observations

flH remains an honestly bounded `40/40` form-only observation set with
`deep_analysis_complete=false`; adding syntax, participant roles, local
context, or ambiguity prose would be new semantic research rather than
maintenance. fwh's `sampling_basis_recorded=false` remains a stored diagnostic
alongside its `UNIVERSAL` exact-set `13/13` coverage and is not an incomplete
coverage finding.

## Future reopening policy

A future proposal may be made only when genuinely new, admitted Quran-internal
evidence exists: a new structural occurrence, corrected morphology/occurrence
identity, a canonical corpus correction, or a methodology revision that
changes a permitted inference. Disagreement with the current result, a new
prompt, external lexical material, tafsir, translation, model memory, or web
retrieval are not reopening evidence. Any permitted proposal starts a new
governed process with fresh preflight, source isolation, evidence, and review;
it does not mutate the closed claim in place or imply acceptance.

## Deferred debt

Extraction-version selection remains deferred pending a canonical ordering and
active-version authority. flH semantic enrichment remains deferred pending a
separately authorized research scope. No migration, semantic record, or Batch
08 work is part of this maintenance change.

## Verification and independent review

- Static checks: `git diff --check`, Ruff for every candidate Python file, and
  bytecode compilation passed.
- Focused checks passed, including 43 isolated regression tests in the fresh
  reviewer context. The disposable governed replay proves convergence remains
  idempotent without touching `lisanapp.db`.
- Full non-E2E regression: `267 passed` (2026-09-14). The remaining 13
  warnings are the Python 3.12 SQLite default-datetime-adapter warning emitted
  by pre-existing migration/test paths in eight test modules; there are no
  remaining `utcnow()` calls in application models, tools, or tests.
- Read-only post-test custody: `lisanapp.db` SHA-256 remained
  `d03d69ca341b01012edd4274840984b43fcf66b59e4a349ae878563fd87b5621`;
  SQLite integrity was `ok`; counts remained 13 ResearchRuns, 607
  ObservationArtifacts, 13 SemanticClaims, 6 VerificationRecords, and 0
  ACCEPTED claims. Batch 07 root artifacts remained byte-identical.
- Fresh independent review cycle 1 returned `PASS / MERGE_READY` for the
  bounded implementation candidate, with no blocker. It is technical review
  evidence only and does not grant release acceptance. The sole nonblocker was
  that the wrong-run negative test detaches the isolation row rather than
  directly mutating the audit entity binding; the implementation validates both
  audit binding fields.
