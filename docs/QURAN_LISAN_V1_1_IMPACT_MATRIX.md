# QURAN_LISAN_V1_1_IMPACT_MATRIX

| PACKAGE_REF | RULE_ID / CONCEPT | IMPLEMENTATION | STATUS | FILES | TESTS | RATIONALE |
|---|---|---|---|---|---|---|
| M01 | Core Methodology | Baseline | IMPLEMENTED | docs/ | test_t01_regression.py | Foundation established |
| R01 | Terminology | Controlled Vocab | IMPLEMENTED | backend/domain/models.py | - | Types enforced via Enum |
| R02 | Research Questions | Schema | IMPLEMENTED | backend/domain/schemas.py | - | Prompts structure |
| R03 | Coverage | CanonicalizationPolicy | IMPLEMENTED | backend/domain/services/ | - | Validated at bounds |
| C01 | Runtime Kernel | Router | NO_RUNTIME_ACTION_REQUIRED | - | - | External runner logic |
| C02 | Reference Cards | Prompts | NO_RUNTIME_ACTION_REQUIRED | - | - | LLM execution context |
| C03 | Composition Guide | UI Rules | NO_RUNTIME_ACTION_REQUIRED | - | - | Formatting guide |
| C04 | Derived Cards | Snapshot Service | IMPLEMENTED | backend/domain/services/ | test_t01_regression.py | Frozen before publishing |
| E01 | Gold Standards | Tests | IMPLEMENTED | scratch/ | - | Benchmark provided |
| A01 | Root Definition | Unity Check | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Enforced via tests |
| A02 | Function vs Form | Null Meaning | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Prevent format as proof |
| A03 | Corpus Coverage | Canonical Check | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Coverage verification |
| A04 | Evidence Chain | Dependency Record | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Revalidation enforces this |
| A05 | Moving Hypothesis | Claim Revision | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Immutable revisions |
| A06 | Empirical Inference | Target Contract | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Rejected circular logic |
| A07 | Slot Filling | Prompting | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Schema constraints |
| A08 | Partial Silence | Semantic Boundary | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Model logic bounds |
| A09 | Antonymy/Relation | Essential Neighbor | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Neighbors required |
| A10 | Circularity | Independent Review | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Separate review stage |
| A11 | Purity | Isolation State | IMPLEMENTED | backend/domain/ | test_t01_regression.py | No leak from outside |
| A12 | Tool Reality | Tool Receipt | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Actual execution track |
| A13 | Isolation | Blind Lab | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Prevent heritage leakage |
| A14 | Output Reality | Research Judgment | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Final claim validation |
| A15 | Memory/Persistence | Semantic Memory | IMPLEMENTED | backend/domain/ | test_t01_regression.py | Admission Gate + Reopen |
