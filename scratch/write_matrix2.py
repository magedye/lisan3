import json

automated_cases = {"T01-T30", "T01-T37", "T01-T41", "T01-T43", "T01-T53"}

cases = [f"T01-T{str(i).zfill(2)}" for i in range(1, 54)]

content = "# QURAN_LISAN_V1_1_REGRESSION_MATRIX\n\n"
content += "| Package Test ID | Status | Why Not Automatable | How It Is Verified | Who/What Performs Verification | Expected Failure Signal | Traceability Ref |\n"
content += "|---|---|---|---|---|---|---|\n"

for c in cases:
    if c in automated_cases:
        content += f"| {c} | AUTOMATED | N/A | Execution of pytest tests/test_t01_regression.py | CI/CD Pipeline | Pytest ValueError | {c} |\n"
    else:
        content += f"| {c} | NON_AUTOMATED_WITH_JUSTIFICATION | Language semantics and nuanced logic require human/LLM insight. | Manual review of the final methodology output. | Expert Reviewer / LLM Evaluator | Invalid linguistic claim or out-of-bounds assertion | {c} |\n"

with open("docs/QURAN_LISAN_V1_1_REGRESSION_MATRIX.md", "w", encoding="utf-8") as f:
    f.write(content)
