# New Lisan Project Reuse & Lessons Kit

## Purpose

This folder is a curated, evidence-based handoff for designing a future **independent** Quran Lisan project. It extracts methods, controls, data concepts, runtime patterns, tests, failures, and open questions from Lisan3 without making them authority for the new project.

This is not a new-project architecture, implementation, migration, refactor, or acceptance decision. Every recommendation remains a proposal for owner review.

## Reviewed repository identity

- Repository: `D:\APP\tafseer\lisanapp3`
- Branch at review start: `main`
- Exact reviewed base HEAD: `5667528297f4f0f3e4b245fa47cec60e992f1798`
- Review start date: 2026-09-05, Asia/Aden
- CodeGraph: unavailable because `.codegraph/` did not exist

## Working-tree state at review start

There were no tracked modifications. Four owner-created paths were already untracked and were treated as protected owner work:

- `.hermes/plans/2026-08-25_lqe-lisan-governed-hybrid-retrieval.md`
- `check_db2.py`
- `debug_proxy.py`
- `run_v4.ps1`

The review did not read these untracked files as evidence and did not modify them.

## Review scope

The review covered 26 source areas spanning policy/authority, canonical methodology, terminology, Quran/corpus admission, morphology, semantic runtime, evidence, counterevidence, falsification, root concept, local meaning, semantic differentiation, source roles, retrieval, AI runtime, Skills, Agent patterns, Tools, domain schemas, confidence/status, Blind Lab, tests/evals, provenance, UX interaction, tooling decisions, and historical lessons.

Evidence strata are kept distinct:

- **Canonical:** current Lisan3 authority within its stated scope.
- **Active derived:** current operating guidance subordinate to canonical authority.
- **Implementation evidence:** what current source code actually enforces or exposes.
- **Test evidence:** what repository tests are designed to prove; current execution is not implied unless a durable report records it.
- **State/evidence report:** candidate-bound or runtime-bound historical evidence; it may be stale relative to current HEAD.
- **Historical:** legacy or superseded material, never current Lisan3 authority.
- **Agent inference:** a recommendation for the new project, not a repository fact.

## Important limitations

- This was repository archaeology, not live semantic research. No Quranic conclusion was generated.
- Existing tests and durable reports were inspected; no Lisan3 product verification or new-project runtime was executed because no existing behavior changed.
- `PROJECT_STATE.md` and `LISAN3_HANDOFF.md` contain time- and candidate-bound history and were checked against current source, but they are not authority.
- Lisan3 has no populated active `registries/` or `schemas/` artifacts at this HEAD; many useful contracts exist instead in Pydantic/SQLAlchemy models and in a legacy reuse package.
- Gem and Opal behavior was not evidenced in this repository. Any assessment of their role is therefore an `OPEN_QUESTION` or agent inference.
- The QAC structural source remains unadmitted in Lisan3. Its Stage-A package is evidence about a candidate and gaps, not permission to reuse or redistribute raw data.
- AI pretrained-knowledge contamination cannot be proven absent merely by prompt rules. The kit recommends risk controls, not a solved detector.

## Navigation

1. Start with [the source inventory](01_SOURCE_INVENTORY.md) and [reuse matrix](02_REUSE_MATRIX.md).
2. For the semantic core, read [terminology](03_TERMINOLOGY_GLOSSARY_CANDIDATES.md), [root concept](04_ROOT_CONCEPT_METHOD_KIT.md), and [semantic layering](05_SEMANTIC_LAYERING_KIT.md).
3. For evidence integrity, read [source control](06_EVIDENCE_AND_SOURCE_CONTROL_KIT.md), [retrieval](10_RETRIEVAL_AND_DISCOVERY_KIT.md), and [confidence/falsification](12_CONFIDENCE_EVALUATION_AND_FALSIFICATION.md).
4. For execution design, read [Skill candidates](07_AI_SKILLS_CANDIDATES/README.md), [Agent orchestration](08_AGENT_ORCHESTRATION_CANDIDATES.md), [Tools/runtime](09_TOOL_AND_RUNTIME_CANDIDATES.md), and [data/schema candidates](11_DATA_AND_SCHEMA_CANDIDATES.md).
5. For decision support, read [tests/evals](13_TESTS_AND_EVALS_REUSE.md), [lessons](14_LESSONS_LEARNED_FROM_LISAN3.md), [anti-reuse](15_DO_NOT_REUSE.md), [gaps](16_GAPS_AND_MISSING_CAPABILITIES.md), and [recommendations](17_RECOMMENDATIONS_FOR_NEW_PROJECT.md).
6. Use [source traceability](18_SOURCE_TRACEABILITY.md) to audit every substantive recommendation.
7. Use the [curated materials index](materials/README.md) for four concise adapted templates and the [verification report](99_VERIFICATION_REPORT.md) for the final scope and integrity checks.
7. `materials/` contains small adapted templates, never authoritative contracts.

## Classification vocabulary

Every matrix candidate has exactly one primary classification: `REUSE_AS_IS`, `ADAPT`, `REFERENCE_ONLY`, `DO_NOT_REUSE`, or `OPEN_QUESTION`. The classification applies only to the proposed new project direction described by the owner.

## Custody rule

All task-authored files are contained in this folder. No commit, push, PR, new-project implementation, or Lisan3 state update is included.
