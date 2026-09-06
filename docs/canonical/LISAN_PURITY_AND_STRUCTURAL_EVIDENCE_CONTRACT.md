# Lisan Methodological Diagnostics and Structural Evidence Contract

Authority revision: `LISAN3_DIAGNOSTICS_CONTRACT_V3_2026_09_06`

## Purpose

This contract preserves useful methodological warnings without making absent
future extractors a universal research lock. Diagnostics guide the AI challenge
cycle, verification, and canonicalization. They do not grant semantic truth.

## Result contract

Each diagnostic returns:

- `EVALUATED_CLEAN`: the available evidence supports the clean rule;
- `FLAGGED`: available evidence indicates the named risk;
- `NOT_EVALUATED`: the required extractor or evidence is absent.

`NOT_EVALUATED` is never clean, but it is not automatically a blocker. A
diagnostic is hard only when its evidence proves violation of a hard boundary
that is material to the current claim. The response identifies the diagnostic,
status, severity, details, evidence references, and whether it is a hard
blocker. Numeric Purity scores and aggregate threshold labels are not authority.

## Diagnostics

| Diagnostic | Risk observed | Default treatment | Hard only when |
|---|---|---|---|
| `DICTIONARY_FIRST` | external frame precedes internal observation | warning/challenge | actual prohibited external content entered internal induction |
| `CONTEXTUAL_LEAKAGE` | evidence falls outside the declared occurrence/window | warning/challenge | asserted support resolves outside the authorized source/scope |
| `HERITAGE_BIAS` | inherited framing substitutes for induction | warning/challenge | prohibited heritage content entered internal induction |
| `TAFSIR_CONTAMINATION` | tafsir supplies the conclusion | warning/challenge | prohibited tafsir content entered internal induction |
| `FORCED_UNIFICATION` | material clusters/counterexamples are erased | warning/challenge | a universal/strong result lacks sufficient coverage or hides resolved counterevidence |
| `GENERIC_OVEREXTRACTION` | the conclusion does not discriminate | warning/challenge | a preferred important result lacks a bounded rejection condition/falsification |
| `LETTER_SEMANTICS_OVERRELIANCE` | speculative letter meaning becomes proof | warning/challenge | the asserted primary evidence is not admitted Quran evidence |
| `CIRCULAR_CONFIRMATION` | a conclusion or derivative supports itself | warning/challenge | asserted support does not terminate in independent resolvable evidence |

Unsupported extractors return `NOT_EVALUATED` and identify the unavailable
capability. They neither fabricate clean evidence nor block unrelated claims.

## Hard source-isolation boundary

Internal Quranic induction permits admitted canonical Quran material and
same-run artifacts only. The host controls context and tools and audits blocked
access. A blocked attempt with no disclosed content is enforcement evidence,
not contamination. Actual disclosed prohibited content marks the run
contaminated and blocks preferred judgment and canonicalization.

## Structural evidence boundary

Tanzil remains authoritative for Quran text and verse identity. Any future QAC
or other structural annotation remains a separate provenance-bound layer keyed
to exact snapshot, verse, word, and segment identity. It cannot mutate Tanzil
text or gain admission through this contract.

When structural evidence is unavailable, the host reports the affected
coverage/validator capability as unavailable. It blocks only a claim whose
scope actually requires that capability. QAC acquisition, persistence,
importer, admission, and activation remain separately governed and outside this
revision.

## Required tests

- blocked external access does not disclose content;
- actual prohibited exposure blocks preferred judgment/canonicalization;
- unsupported diagnostics remain visible but non-blocking;
- missing or cross-run evidence is rejected;
- incomplete universal coverage is rejected while a valid local scope is not;
- circular/fabricated evidence cannot qualify a result;
- no diagnostic can set canonical acceptance.
