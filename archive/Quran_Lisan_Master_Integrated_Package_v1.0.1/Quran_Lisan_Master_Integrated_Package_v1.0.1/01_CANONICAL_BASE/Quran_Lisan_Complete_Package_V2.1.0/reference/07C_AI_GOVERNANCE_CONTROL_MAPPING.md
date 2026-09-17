# خريطة تحويل دستور حوكمة الذكاء الاصطناعي إلى ضوابط تنفيذية

**الإصدار:** 2.1.0  
**الحالة:** `CANONICAL_GOVERNANCE_MAPPING`

## 1. الغرض
هذه الوثيقة تمنع بقاء الدستور نصًا إرشاديًا فقط. كل مبدأ حرج يجب أن يظهر في واحد أو أكثر من: Control، Requirement، Schema، Skill، Tool Permission، Gate، Validator، Test، أو Authorization contract.

## 2. السلسلة الحاكمة
```text
Constitutional Principle
    ↓
Policy / Control
    ↓
Requirement
    ↓
Skill / Tool / Workflow / Gate
    ↓
Record / Receipt
    ↓
Test
    ↓
Acceptance Evidence
```

## 3. التحويلات ذات الأولوية
| المبدأ | التنفيذ الحاكم في V2.1 | دليل التنفيذ |
| --- | --- | --- |
| معرفة النموذج ليست دليلًا | Source policy + CTL-006/CTL-024/CTL-026 | SourceAccessEvent, EvidenceRelation |
| المصدر يسبق الاستنتاج | Source Gate + Internal phase isolation | SourceIdentity, InternalSnapshot |
| التوجيه ليس إنفاذًا | Tool Gateway + Validators + State Machine | ExecutionReceipt, tests |
| الحرية داخل الحدود | Skills + allowed tools/phases | Skill contracts, TOOL_REGISTRY |
| المشاهدة ≠ الفرضية ≠ الحكم | Observation/Hypothesis/SemanticDecision | JSON Schemas |
| الدحض إلزامي | Falsification Gate + SK-10 | FalsificationRun |
| التغطية قبل التعميم | Coverage Gate | CompletenessProfile |
| Claim → Evidence | Evidence Gate | EvidenceRelation |
| الحكم البحثي ≠ الاعتماد | `SemanticDecision.authority_level=RESEARCH_JUDGMENT` + CanonicalAuthorization | Schemas + GOV tests |
| تحقق مستقل ≠ مراجعة ذاتية | IndependentVerification | Verification schema/receipts |
| consensus ليس Evidence | CTL-045 + MOA contract | MOADeepReviewReport validator |
| ثقة النموذج ≠ قوة النتيجة | CTL-020/021/022 | ConfidenceComponent + CompletenessProfile |
| لا Framework هو المنهج | NFR-005 + CAP-GO fallback | package architecture tests |

## 4. البوابات الأربع الدنيا
تبقى النواة الدنيا: `Source Gate`, `Coverage Gate`, `Evidence Gate`, `Falsification Gate`. ولا تُسمى أي تعليمات نصية «Gate» إلا إذا كان الـHost قادرًا فعليًا على منع المرور.

## 5. سلطة الحكم البحثي
`SemanticDecision` هو **حكم بحثي** صادر بعد تحليل الأدلة والبدائل والدحض ضمن المنهج. يمكن أن يكون `PREFERRED` أو `UNRESOLVED` أو غير ذلك، لكنه لا يحمل سلطة الاعتماد الرسمي. إذا كانت النتيجة مرشحة للدخول إلى معرفة المشروع الرسمية، ينشأ `CanonicalAuthorization` مستقل يربط الحكم الذي راجعه، نوع المراجع، القرار، وأثره.

## 6. قاعدة عدم التكرار
لا تنشأ منظومة حوكمة ثانية موازية؛ هذا الدستور يفسر ويعلو على ضوابط V2 القائمة، والسجلات الآلية هي الصورة التنفيذية المختصرة. أي إضافة لاحقة يجب أن توسع السجلات الحالية بدل نسخها في Registry جديد غير مترابط.
