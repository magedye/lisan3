import re

with open('scratch/Quran-Lisan-v1.1/Quran-Lisan-v1.1/04-Tests/T01 — Regression & Adversarial Test Suite.md', 'r', encoding='utf-8') as f:
    content = f.read()

cases = re.findall(r'#### (T01-T\d+) — (.*?)\n\*\*Stimulus:\*\* (.*?)\n\*\*Expect:\*\* (.*?)\n\*\*Covers:\*\* (.*?)\n', content, re.DOTALL)
# some cases might not have all fields. Let's make it more robust.

blocks = re.split(r'#### T01-T', content)
cases = []
for block in blocks[1:]:
    if not block[0].isdigit():
        continue
    id_num = block[:2]
    full_id = f'T01-T{id_num}'
    
    title_match = re.search(r' — (.*?)\n', block)
    threat = title_match.group(1).strip() if title_match else ''
    
    expect_match = re.search(r'\*\*Expect:\*\* (.*?)\n', block)
    expect = expect_match.group(1).strip() if expect_match else ''
    
    covers_match = re.search(r'\*\*Covers:\*\* (.*?)\n', block)
    covers = covers_match.group(1).strip() if covers_match else ''
    
    cases.append({
        'id': full_id,
        'threat': threat,
        'expect': expect,
        'covers': covers
    })

matrix_lines = [
    '# QURAN_LISAN_V1_1_REGRESSION_MATRIX',
    '',
    '| Package ID | Threat | LISAN3 Control | Automated Test | Status | Notes |',
    '|---|---|---|---|---|---|'
]

for case in cases:
    # All cases are unaccounted for initially as we need to write tests
    matrix_lines.append(f"| {case['id']} | {case['threat']} | {case['covers']} | TBD | NON_AUTOMATED_WITH_JUSTIFICATION / UNACCOUNTED | Needs Implementation |")

with open('docs/QURAN_LISAN_V1_1_REGRESSION_MATRIX.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(matrix_lines))

print(f"Generated matrix with {len(cases)} cases.")
