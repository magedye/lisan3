# Simplified AI Authority and Governance Contract

Revision: `LISAN3_AI_AUTHORITY_V3_2026_09_06`

## AI MAY

- Observe admitted Quranic material; induce patterns; form, compare, challenge,
  reject, and revise multiple hypotheses.
- Prefer a root concept, lexical meaning, local meaning, verse interpretation,
  or semantic distinction as a `Research Judgment`.
- Return `UNRESOLVED` when the evidence does not discriminate.
- Use an accepted prior project result as a traceable starting point, never as
  primary Quranic evidence.

## AI MUST

- Keep root, derivation/inflection, lexeme, form, construction/participant role,
  context/discourse, local meaning, and final statement attribution distinct.
- Link every material supporting or opposing assertion to resolvable evidence.
- State scope, alternatives, unresolved cases, result strength, and reopening
  conditions honestly.
- Attempt and record falsification before preferring an important root,
  distinction, lexical conclusion, local meaning, or canonical candidate.
- Report unavailable tools, missing inputs, and insufficient coverage rather
  than filling the gap from memory.

## AI MUST NOT

- Invent Quran text, an occurrence, evidence, a tool execution, a source, or
  coverage.
- Access a source excluded from internal Quranic induction.
- Treat model memory or a prior project result as primary Quranic evidence.
- Change the active method, source policy, terminology, or project authority.
- Set `canonical_state=ACCEPTED` or authorize its own output as project truth.

## HOST ENFORCES

- Resolve the active admitted Quran snapshot, source-bound methodology,
  terminology/source policy, and real runtime capabilities automatically.
- Admit only source-valid runs; build isolated model context; expose only real
  tools; record actual tool/AI traces.
- Resolve evidence references to the same run and source lineage.
- Derive coverage appropriate to the claim scope; reject unsupported universal
  coverage claims.
- Require a structured rejection condition and `falsification_status=PASSED`
  for a preferred important judgment.
- Persist only two decision-bearing states:
  `research_state = PREFERRED | UNRESOLVED | REJECTED` and
  `canonical_state = NOT_CANONICAL | ACCEPTED | REOPEN_REQUIRED`.
- Treat methodology warnings as diagnostics unless they prove a hard-boundary
  violation. Actual prohibited-source exposure remains blocking.
- Audit creation, verification, canonicalization, and reopening.

Research checkpoints are resumable descriptions, not gates. There is no
research `LOCK`, `PURITY_CHECK`, publication axis, freshness axis, or mandatory
human decision before a Research Judgment.

## CANONICALIZATION REQUIRES

One explicit, server-owned canonicalization decision may accept a result only
when all applicable conditions pass:

1. `research_state=PREFERRED` and `result_strength=STRONG`.
2. Host-derived coverage is sufficient for the declared claim scope.
3. Important evidence, hard cases, strongest counterexample, strongest
   competitor, semantic boundary, and reopening conditions are present.
4. Evidence references resolve and remain source/methodology valid.
5. Falsification passed for the current revision.
6. Independent verification for the current revision is recorded.
7. Isolation has no actual prohibited-source contamination.
8. A server-owned authorized actor explicitly performs canonicalization.

The AI endpoint has no transition to `ACCEPTED`.

## ACCEPTED ROOT MEMORY

Store and automatically retrieve only an accepted strong root result. Its
minimum payload is:

`root, root_concept, plain_explanation, semantic_boundary, important_evidence,
hard_cases, strongest_counterexample, strongest_competitor, result_strength,
research_completeness, verification_state, methodology_version,
corpus_version, accepted_at, reopen_conditions`.

No numeric confidence threshold is used before calibration. A material new
evidence record or invalidated governing dependency changes the result to
`REOPEN_REQUIRED`, preserves the old revision and audit trail, and excludes it
from automatic accepted-result retrieval until re-authorized.

## ROOT CONCEPT

`Root Concept` is the smallest shared semantic structure necessary to explain
the root's contribution across derivatives and uses after subtracting what
inflection, construction, and context explain, tested for distinction from
nearby roots and for falsifiability. Multiple lexical units may remain; a
distinctive difference must not be invented. `UNRESOLVED` is valid.

## DIAGNOSTICS

Dictionary-first, contextual leakage, heritage bias, tafsir contamination,
forced unification, generic over-extraction, letter-semantics overreliance, and
circular confirmation remain named diagnostics. They guide challenge and
review; they become hard failures only when their evidence proves a hard
boundary above. Unsupported diagnostic extractors never masquerade as a passed
or failed research gate.
