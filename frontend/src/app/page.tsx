"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { ResearchStatus } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import { useApiResource } from "@/lib/use-api-resource";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

type AskResponse = components["schemas"]["AskLisanResponse"];
type AttentionResponse = components["schemas"]["AttentionCenterResponse"];
type ResearchRun = components["schemas"]["ResearchRunResponse"];

export default function AttentionCenter() {
  const attention = useApiResource<AttentionResponse>("/api/attention");
  const [expression, setExpression] = useState("");
  const [contractType, setContractType] = useState("ROOT_CONCEPT");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<AskResponse | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const router = useRouter();

  async function handleAsk(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setResult(null);
    setActionError(null);
    try {
      const response = await apiFetch<AskResponse>("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression, contract_type: contractType }),
      });
      setResult(response);
    } catch (reason) {
      setActionError(reason instanceof Error ? reason.message : "تعذر الاتصال بالخدمة الخلفية.");
    } finally {
      setSubmitting(false);
    }
  }

  async function startResearch() {
    if (!data?.run_admission.available) {
      setActionError("إنشاء تشغيل بحث غير متاح حتى تُقبل موارد Corpus والمنهجية من السلطة الحالية.");
      return;
    }
    setSubmitting(true);
    setActionError(null);
    try {
      const run = await apiFetch<ResearchRun>("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_contract: contractType,
          target_expression: expression,
        }),
      });
      router.push(`/run/${run.id}`);
    } catch (reason) {
      setActionError(reason instanceof Error ? reason.message : "تعذر إنشاء تشغيل البحث.");
      setSubmitting(false);
    }
  }

  const data = attention.data;

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="RES-HOME-01 · Golden Production"
        title="مركز الانتباه — اسأل لسان (Ask Lisan)"
        description="نقطة دخول إلى البحث المحكوم: بيانات الانتباه من الحالة المحفوظة، والإجابة من العقود القائمة فقط."
        actions={<span className="status-badge status-positive"><span aria-hidden="true">●</span> بيانات فعلية فقط</span>}
      />

      {attention.loading && <LoadingState label="جارٍ تجميع مركز الانتباه من السجلات الفعلية…" />}
      {attention.error && <ErrorState message={attention.error} retry={attention.reload} />}
      {data && (
        <>
          <section className="metric-grid" aria-label="ملخص الانتباه الفعلي">
            <article className="metric-card information">
              <span>أحدث تشغيلات البحث</span>
              <strong>{data.recent_runs.length}</strong>
              <small>معروضة من ResearchRun المحفوظ</small>
            </article>
            <article className="metric-card warning">
              <span>مرشحة للاعتماد</span>
              <strong>{data.canonicalization_candidates.length}</strong>
              <small>نتائج قوية بعد البحث، لا تتطلب قراراً أثناء البحث</small>
            </article>
            <article className="metric-card stale">
              <span>أعيد فتحها</span>
              <strong>{data.reopen_required_claims.length}</strong>
              <small>REOPEN_REQUIRED بسبب دليل أو حاكم جديد</small>
            </article>
            <article className="metric-card positive">
              <span>مقترحات حوكمة معلقة</span>
              <strong>{data.pending_proposals.length}</strong>
              <small>PROPOSED فقط</small>
            </article>
          </section>

          <div className="two-column">
            <Panel title="أبحاث حديثة" eyebrow="Resume · Durable Runs">
              {data.recent_runs.length === 0 ? (
                <EmptyState title="لا توجد تشغيلات بحث" detail="أنشئ تشغيلاً من مسار عدم كفاية الأدلة أدناه." />
              ) : (
                <div className="stack">
                  {data.recent_runs.map((run) => (
                    <Link key={run.id} href={`/run/${run.id}`} className="list-card">
                      <strong>{run.target_expression}</strong>
                      <span>{run.current_stage} · {run.status}</span>
                      <small className="technical-text">{run.id} · {run.methodology_revision}</small>
                    </Link>
                  ))}
                </div>
              )}
            </Panel>

            <Panel title="تغيّرات حديثة" eyebrow="Audit-backed">
              {data.recent_changes.length === 0 ? (
                <EmptyState title="لا توجد أحداث مسجلة" detail="لن تملأ الواجهة هذا القسم بسجلات تجريبية." />
              ) : (
                <div className="stack">
                  {data.recent_changes.slice(0, 5).map((event) => (
                    <div className="list-card" key={event.id}>
                      <strong>{event.action}</strong>
                      <span>{event.entity_type}</span>
                      <small>{new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(event.created_at))}</small>
                    </div>
                  ))}
                </div>
              )}
            </Panel>
          </div>
        </>
      )}

      <Panel title="اسأل عن لفظ أو جذر" eyebrow="Governed Ask" className="ask-workspace">
        <form onSubmit={handleAsk} className="form-grid form-grid-3" id="ask">
          <label className="form-field">
            <span>اللفظ المستهدف</span>
            <input
              id="ask-expression"
              name="expression"
              className="input"
              type="text"
              value={expression}
              onChange={(event) => setExpression(event.target.value)}
              placeholder="e.g. ضرب"
              required
            />
          </label>
          <label className="form-field">
            <span>نوع العقد الدلالي</span>
            <select id="ask-contract" name="contract_type" className="select" value={contractType} onChange={(event) => setContractType(event.target.value)}>
              <option value="ROOT_CONCEPT">مفهوم الجذر (Root Concept)</option>
              <option value="LEXEME">معنى المفردة العام</option>
              <option value="LOCAL_MEANING">المعنى الموضعي (Local Meaning)</option>
              <option value="VERSE_MEANING">معنى الآية</option>
              <option value="SEMANTIC_DIFFERENCE">الفرق بين مفردتين</option>
            </select>
          </label>
          <div className="form-field">
            <span aria-hidden="true">&nbsp;</span>
            <button type="submit" disabled={submitting} className="button button-primary">
              {submitting ? "جارٍ البحث…" : "Search — بحث"}
            </button>
          </div>
        </form>

        {actionError && <div className="state-card error-state" role="alert"><strong>تعذر إكمال الإجراء</strong><p>{actionError}</p></div>}

        {result?.status === "INSUFFICIENT_EVIDENCE" && data && (
          <section className="panel panel-warning" aria-labelledby="insufficient-title">
            <h3 id="insufficient-title">Insufficient Evidence — الأدلة الحالية غير كافية</h3>
            <p>لا توجد نتيجة بحثية مفضلة أو نتيجة معتمدة للفظ <strong>{expression}</strong> ضمن العقد <span className="technical-text">{contractType}</span>. لا تُنشئ الواجهة جواباً بديلاً.</p>
            {!data.run_admission.available ? (
              <div id="run-admission-unavailable" className="state-card" role="status">
                <strong>Run Builder unavailable — موارد البحث غير مقبولة حالياً</strong>
                <ul>{data.run_admission.blockers.map((blocker) => <li key={blocker}>{blocker}</li>)}</ul>
                <p>المضيف يحل Corpus والمنهجية الفعليين؛ غياب سلطة صالحة يمنع التشغيل.</p>
              </div>
            ) : (
              <div className="button-row">
                <button type="button" onClick={startResearch} className="button button-secondary" disabled={submitting}>Start Research Run — ابدأ تشغيل بحث</button>
                <small>سيحل المضيف المصدر والمنهجية وسياسة العزل تلقائياً.</small>
              </div>
            )}
          </section>
        )}

        {(result?.status === "ACCEPTED_RESULT" || result?.status === "PREFERRED_RESEARCH_RESULT") && result.claim && (
          <section className="panel panel-information found-panel">
            <div className="panel-heading">
              <div><span className="eyebrow">Research Judgment</span><h2>{result.status === "ACCEPTED_RESULT" ? "نتيجة معتمدة" : "ترجيح بحثي"}</h2></div>
              <Link className="button button-secondary button-small" href={`/claims/${result.claim.id}`}>فتح التتبّع الكامل</Link>
            </div>
            <ResearchStatus
              research={result.claim.research_state}
              canonical={result.claim.canonical_state}
              strength={result.claim.result_strength}
              verification={result.claim.verification_state}
            />
          </section>
        )}
      </Panel>
    </main>
  );
}
