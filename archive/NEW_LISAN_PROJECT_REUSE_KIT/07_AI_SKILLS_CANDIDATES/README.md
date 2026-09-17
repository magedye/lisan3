# AI Skill Candidates

These are concise candidate protocols, not installed Skills and not accepted new-project method. They extract tasks from `skills/lisan-semantic-extraction/SKILL.md`, current domain contracts, source controls and tests. Each has exactly one reuse classification.

| Skill | Classification | Main reason |
|---|---|---|
| [Analysis-unit resolution](01_ANALYSIS_UNIT_RESOLUTION.md) | `ADAPT` | Preserve scoping, add lexical-unit and ambiguity support. |
| [Quran occurrence collection](02_QURAN_OCCURRENCE_COLLECTION.md) | `REUSE_AS_IS` | Deterministic, source-bound collection is foundational. |
| [Derivational-family analysis](03_DERIVATIONAL_FAMILY_ANALYSIS.md) | `ADAPT` | Lisan3 method is useful; active runtime lacks structural support. |
| [Morphological-form analysis](04_MORPHOLOGICAL_FORM_ANALYSIS.md) | `ADAPT` | Must separate structural fact from semantic operator judgment. |
| [Root-concept extraction](05_ROOT_CONCEPT_EXTRACTION.md) | `ADAPT` | AI may issue a bounded preferred conclusion in the new project. |
| [Local-meaning analysis](06_LOCAL_MEANING_ANALYSIS.md) | `ADAPT` | Preserve layers, simplify governance. |
| [Construction analysis](07_CONSTRUCTION_ANALYSIS.md) | `ADAPT` | Needs provenance-bound syntax and explicit ambiguity. |
| [Semantic-neighbor comparison](08_SEMANTIC_NEIGHBOR_COMPARISON.md) | `ADAPT` | Add multidimensional distance and no-difference outcome. |
| [Distinctive-feature discovery](09_DISTINCTIVE_FEATURE_DISCOVERY.md) | `ADAPT` | Preserve positive residue, prohibit forced distinction. |
| [Competing-hypothesis generation](10_COMPETING_HYPOTHESIS_GENERATION.md) | `ADAPT` | Keep serious alternatives, avoid ceremonial alternatives. |
| [Falsification/counterevidence](11_FALSIFICATION_AND_COUNTEREVIDENCE.md) | `REUSE_AS_IS` | Operational rejection and hard-case search remain essential. |
| [Source-contamination review](12_SOURCE_CONTAMINATION_REVIEW.md) | `ADAPT` | Extend source logs to pretrained-exposure uncertainty. |
| [Result synthesis](13_RESULT_SYNTHESIS.md) | `ADAPT` | AI can decide, but result must expose basis and limits. |

All Skills must emit structured artifacts and never claim a Tool ran without a server-owned receipt. [TR-050]
