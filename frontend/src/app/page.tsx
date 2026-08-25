"use client";

import type { components } from "@/api/openapi";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

type AskResponse = components["schemas"]["AskLisanResponse"];

export default function AttentionCenter() {
  const [expression, setExpression] = useState("");
  const [contractType, setContractType] = useState("ROOT_CORE");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AskResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleAsk = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression, contract_type: contractType }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setResult((await response.json()) as AskResponse);
    } catch {
      setError("تعذّر الاتصال بالخدمة الخلفية. تحقّق من جاهزية قاعدة البيانات.");
    } finally {
      setLoading(false);
    }
  };

  const startResearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_contract: contractType,
          target_expression: expression,
          methodology_revision: "v7.1",
          corpus_snapshot: "current",
          authority_context: { initiator: "local_user" },
        }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const runData = (await response.json()) as { id: string };
      router.push(`/run/${runData.id}`);
    } catch {
      setError("تعذّر إنشاء مسار البحث. لم تُكتب حالة بحث جديدة.");
      setLoading(false);
    }
  };

  return (
    <main className="page-frame">
      <section className="page-heading">
        <div>
          <span className="eyebrow">Golden UX · Attention Center</span>
          <h1>مركز الانتباه — اسأل لسان (Ask Lisan)</h1>
          <p>ابدأ من سؤال موثّق، ثم انتقل إلى مسار بحث محكوم عند غياب الدليل.</p>
        </div>
        <span className="truth-badge">لا بيانات نموذجية</span>
      </section>

      <section className="attention-grid" aria-label="ملخص مركز الانتباه">
        <article className="attention-card attention-notice">
          <span className="card-kicker">التنبيهات التشغيلية</span>
          <strong>عقد قراءة مركز الانتباه غير متاح بعد</strong>
          <p>لن تعرض الواجهة مهام أو أرقامًا افتراضية. استخدم المسارات الفعلية أدناه.</p>
        </article>
        <Link className="attention-card linked-card" href="/audit">
          <span className="card-kicker">قابل للتتبع</span>
          <strong>سجل التدقيق</strong>
          <p>اقرأ أحداث النظام المسجلة من واجهة التدقيق الفعلية.</p>
        </Link>
        <Link className="attention-card linked-card" href="/governance">
          <span className="card-kicker">ضوابط مستقلة</span>
          <strong>مركز الحوكمة</strong>
          <p>راجع المقترحات وسجل المراجعات دون اختزال حالات السلطة.</p>
        </Link>
      </section>

      <section className="ask-panel">
        <div className="section-title">
          <div>
            <span className="eyebrow">مدخل بحث فعلي</span>
            <h2>اسأل عن لفظ أو جذر</h2>
          </div>
          <span className="contract-note">بحث عقدي، لا إجابة مولّدة</span>
        </div>

        <form onSubmit={handleAsk} className="ask-form">
          <label>
            <span>اللفظ المستهدف</span>
            <input
              type="text"
              value={expression}
              onChange={(event) => setExpression(event.target.value)}
              placeholder="e.g. ضرب"
              required
            />
          </label>
          <label>
            <span>نوع العقد الدلالي</span>
            <select value={contractType} onChange={(event) => setContractType(event.target.value)}>
              <option value="ROOT_CORE">المعنى المحوري (Root Core)</option>
              <option value="LOCAL_MEANING">المعنى الموضعي (Local Meaning)</option>
            </select>
          </label>
          <button type="submit" disabled={loading} className="primary-action">
            {loading ? "Searching..." : "Search — بحث"}
          </button>
        </form>

        {error && <div className="result-panel error-panel" role="alert">{error}</div>}

        {result?.status === "INSUFFICIENT_EVIDENCE" && (
          <div className="result-panel evidence-gap">
            <h3>Insufficient Evidence — الدليل غير كافٍ</h3>
            <p>
              لا توجد دعوى دلالية مقفلة للفظ <strong>{expression}</strong> ضمن العقد {contractType}.
            </p>
            <button onClick={startResearch} className="secondary-action" disabled={loading}>
              Start Research Run — ابدأ مسار بحث
            </button>
          </div>
        )}

        {result?.status === "FOUND" && result.claim && (
          <div className="result-panel found-panel">
            <h3>دعوى دلالية موجودة</h3>
            <dl className="state-grid">
              <div><dt>المعرف</dt><dd>{result.claim.id}</dd></div>
              <div><dt>المعرفي</dt><dd>{result.claim.epistemic_state}</dd></div>
              <div><dt>المراجعة</dt><dd>{result.claim.review_state}</dd></div>
              <div><dt>الحداثة</dt><dd>{result.claim.freshness_state}</dd></div>
              <div><dt>النشر</dt><dd>{result.claim.publication_state}</dd></div>
            </dl>
          </div>
        )}
      </section>
    </main>
  );
}
