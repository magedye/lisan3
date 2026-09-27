content = '''# QURAN_LISAN_V1_1_IMPACT_MATRIX

| Package Ref | Rule | LISAN3 Mapping | Implementation Status | Files | Tests | Notes |
|-------------|------|----------------|-----------------------|-------|-------|-------|
| M01 | Core Methodology | - | ALREADY_IMPLEMENTED | docs/ | - | Baseline established |
| A01 | Root Definition | test_root_semantic_unity | ALREADY_IMPLEMENTED | tests/ | test_root_canonicalization | Unity check works |
| A02 | Function vs Form | - | NON_AUTOMATED_WITH_JUSTIFICATION | - | - | Needs LLM review |
| A03 | Corpus Coverage | CanonicalizationPolicy | ALREADY_IMPLEMENTED | backend/domain/ | test_canonical_runtime_qualification | coverage checked |
| A04 | Evidence Chain | DependencyRecord | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Derived cards bounded |
| A05 | Moving Hypothesis | ClaimRevision | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Immutable revisions |
| A06 | Empirical Inference| Target Contract | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Rejected circular |
| A07 | Slot Filling | - | NON_AUTOMATED_WITH_JUSTIFICATION | - | - | Prompt-level |
| A08 | Partial Silence | SemanticBoundary | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Absence!=Exclusion |
| A09 | Antonymy/Relation | EssentialNeighbor | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Unresolved check |
| A10 | Circularity | - | NON_AUTOMATED_WITH_JUSTIFICATION | - | - | Prompt-level |
| A11 | Purity | IsolationState | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Fully bounded |
| A12 | Tool Reality | ToolReceipt | NEWLY_IMPLEMENTED | backend/domain/ | test_t01_regression.py | Enforced strictly |
| A13 | Isolation | - | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | Isolation rules |
| A14 | Output Reality | ResearchJudgment | ALREADY_IMPLEMENTED | backend/domain/ | tests/ | - |
| A15 | Memory/Persistence | SemanticMemoryService | NEWLY_IMPLEMENTED | backend/domain/ | test_t01_regression.py | Memory Gate + Reopen |
| R01-R03 | Root Ops | - | ALREADY_IMPLEMENTED | - | - | - |
| C01-C04 | Canonicalization| InternalSnapshotService| NEWLY_IMPLEMENTED | backend/domain/ | test_t01_regression.py | Immutable snapshot |
| T01 | Regression Tests | test_t01_regression.py | ALREADY_IMPLEMENTED | tests/ | test_t01_regression.py | Matrix built |
| E01 | Exemplars | - | ALREADY_IMPLEMENTED | - | - | - |
'''

with open('docs/QURAN_LISAN_V1_1_IMPACT_MATRIX.md', 'w', encoding='utf-8') as f:
    f.write(content)
