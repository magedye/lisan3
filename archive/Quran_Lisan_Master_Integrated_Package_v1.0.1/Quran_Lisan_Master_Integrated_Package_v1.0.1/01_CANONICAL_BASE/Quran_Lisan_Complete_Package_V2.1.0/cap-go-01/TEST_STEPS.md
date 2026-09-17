# خطوات CAP-GO-01

## CAP-GO-01-01 — Tool allowlist enforcement
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: Tool خارج allowlist يفشل ولا يدعي الوكيل نجاحه.
6. Save evidence file hashes in the report.

## CAP-GO-01-02 — Server-owned execution receipt
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: كل Tool call يعاد معه receipt يمكن readback والتحقق من digest.
6. Save evidence file hashes in the report.

## CAP-GO-01-03 — Structured output external validation
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: unknown field يرفض خارج المنصة.
6. Save evidence file hashes in the report.

## CAP-GO-01-04 — Stable run/artifact IDs
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: IDs تصدر وتقرأ بعد الجلسة.
6. Save evidence file hashes in the report.

## CAP-GO-01-05 — Resume with lineage
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: استئناف run لا يفقد lineage.
6. Save evidence file hashes in the report.

## CAP-GO-01-06 — Branch and join
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: فرضان متنافسان يبقيان منفصلين حتى join دون overwrite.
6. Save evidence file hashes in the report.

## CAP-GO-01-07 — Internal source isolation
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: external tool/index محظور فعليا في INTERNAL_ANALYSIS.
6. Save evidence file hashes in the report.

## CAP-GO-01-08 — Immutable internal snapshot
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: بعد الإغلاق لا يعدل snapshot عند فتح external.
6. Save evidence file hashes in the report.

## CAP-GO-01-09 — Retry lineage/idempotency
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: retry لا ينشئ SemanticDecision مكررًا.
6. Save evidence file hashes in the report.

## CAP-GO-01-10 — Model/config/memory influence logging
1. Reset/clone fixture environment.
2. Apply the matching fixture input.
3. Execute the target capability once, then repeat where idempotency/readback matters.
4. Export/read back the relevant artifact/receipt.
5. PASS only if: يسجل ما تسمح المنصة به من model/config/memory influence.
6. Save evidence file hashes in the report.
