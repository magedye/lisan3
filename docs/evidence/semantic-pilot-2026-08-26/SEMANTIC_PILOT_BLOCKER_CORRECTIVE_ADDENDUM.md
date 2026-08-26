# Semantic-Pilot Blocker Corrective Addendum

Date: 2026-08-26
Original evidence candidate: `6b5313b7696f01a54f76cb907cd722f822ff22ae`
Independent review verdict: `SEMANTIC_PILOT_BLOCKER_VERDICT_NOT_CONFIRMED`
Readiness preserved: `SEMANTIC_PILOT_BLOCKED`

## Evidence boundary

This is an additive correction to
`SEMANTIC_PILOT_BLOCKER_REPORT.md`. The original report and every artifact named
by `artifact-hashes.json` remain byte-for-byte historical evidence. This
addendum corrects current interpretation and classification; it does not alter
the five ResearchRuns, their persisted state, or any original evidence fact.

The review did not contradict the five-root evidence integrity. Preserve:

- ع د ل / `run_d7519288`, أ م ن / `run_8d696d64`, س ل م /
  `run_1a24ffab`, ح م د / `run_68c7b72c`, and ش ك ر /
  `run_5f72ad9d`;
- `LOCK_BLOCKED`, `root_core: null`, and occurrence coverage `NOT_VERIFIED`;
- clean IsolationState plus the recorded blocked prior-semantic access attempts;
- no fabricated semantic evidence and no rerun;
- `DO_NOT_START_REMAINING_BATCHES`.

## Corrected blocker decomposition

### 1. Authority and provenance

The original report incorrectly described QAC as admitted. The conflict was
`AUTHORITY_CONFLICT`; the current canonical reconciliation resolves it
fail-closed. QAC is `PENDING_ADMISSION` / `SOURCE_ROLE_PENDING`, its structural
role is `NOT_APPROVED`, and its provenance/license evidence is `PENDING`.
Closing those open facts requires exact external evidence and a later explicit
owner admission decision; neither is supplied by this addendum.
The later decision must follow separate artifact qualification,
domain/persistence capability, and real-importer validation evidence; none of
those prerequisites pre-authorizes its result.

### 2. Physical artifact

No exact governed QAC artifact, version/release identity, byte size, format, or
expected SHA-256 exists in this repository candidate. This is an
`EXTERNAL_DEPENDENCY`; historical external artifacts are not evidence for this
candidate.

### 3. Real-format importer

The current QAC adapter parses only a synthetic pipe-delimited fixture shape,
and fixture import discards the parsed structural annotations. A deterministic
real-format parser, prohibited-field rejection, multi-segment preservation,
Tanzil reconciliation, lineage, and idempotency proof are absent. This missing
product capability is `PRODUCT_DEFECT` for semantic-pilot enablement, although
implementing it was not authorized in the evidence run or this governance task.

### 4. Domain and persistence

Current `CorpusOccurrence` is verse-level and carries only snapshot, expression,
verse reference, and text. `CorpusSnapshot` carries only descriptive structural
source/version strings. There is no provenance-bound annotation model for word
and segment identity, root, lemma, POS, form, voice/features, permitted syntax,
or source row lineage. This is a separate `PRODUCT_DEFECT` for enablement. The
future boundary is defined in
`docs/canonical/LISAN_PURITY_AND_STRUCTURAL_EVIDENCE_CONTRACT.md`.

### 5. Research evidence

Because authority, artifact, importer, and persistence prerequisites are open,
exact root occurrence coverage cannot be established. For the five runs this is
the fail-closed research result `NOT_VERIFIED`, not evidence that morphology was
evaluated and failed and not an additional external artifact claim.

### 6. Purity capability

Purity is an independent semantic/Internal-Lock blocker. All eight mandatory
dimensions returned `NOT_EVALUATED`; only `DICTIONARY_FIRST` has a partial
timestamp heuristic and its full access-lineage contract is still absent. The
other seven lack supported evaluators. This is `PRODUCT_DEFECT` for enablement,
while the existing refusal to treat non-clean dimensions as passed is correct.

## ROOT_CARD / TERM_CARD correction

ROOT_CARD and TERM_CARD are not consulted by corpus analysis,
`PURITY_CHECK`, or `INTERNAL_LOCK`. Their absence is therefore not a semantic or
Internal-Lock blocker. `DERIVED_PRESENTATION_CONTRACT_GAP` is used here only as
a descriptive planning category, not a persisted lifecycle, gate, or epistemic
status. If later authorized, cards remain derived read-model/publication/UI/API
work and cannot originate or confirm semantic claims.

## Gate interpretation

- Corpus prerequisite: passed for the bound production Tanzil snapshot.
- Blind Lab isolation prerequisite: passed and quarantine enforcement was
  evidenced for all five runs.
- Purity prerequisite: failed for all five because every dimension was
  `NOT_EVALUATED`.
- Internal Lock: correctly failed as a direct consequence of Purity.
- Exact occurrence/root evidence: an upstream research-enablement prerequisite,
  not a separate condition currently evaluated by `INTERNAL_LOCK`.
- ROOT_CARD / TERM_CARD: not a gate prerequisite.

## Current reopening rule

Do not rerun the five roots and do not start remaining batches. The same
five-root pilot may be rerun only after a bounded enabling candidate closes the
required structural and Purity capabilities and that exact candidate is freshly
and independently accepted for the intended profile.
