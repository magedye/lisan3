"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { StatusAxes, StatusBadge } from "@/components/status-axes";
import { useApiResource } from "@/lib/use-api-resource";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";

type Workspace = components["schemas"]["RunWorkspaceResponse"];
type View = "overview" | "artifacts" | "gates";

const stages = [
  "PREFLIGHT",
  "ISOLATION_PREFLIGHT",
  "CORPUS_COLLECTION",
  "STRUCTURAL_OBSERVATION",
  "HYPOTHESIS_GENERATION",
  "DIFFERENTIATION",
  "LOCKING",
];

export default function ResearchRunPage() {
  const params = useParams();
  const runId = params.id as string;
  const workspace = useApiResource<Workspace>(`/api/runs/${runId}/workspace`);
  const [view, setView] = useState<View>("overview");

  if (workspace.loading) return <main className="page-frame"><LoadingState label="جارٍ استعادة تشغيل البحث من الحالة المحفوظة…" /></main>;
  if (workspace.error || !workspace.data) return <main className="page-frame"><ErrorState message={workspace.error ?? "Run not found."} retry={workspace.reload} /></main>;

  const data = workspace.data;
  const run = data.run;

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="RES-RUN-DETAIL · Persisted Workspace"
        title={`تشغيل البحث: ${run.target_expression}`}
        description="مساحة بحث مستأنفة من SQLite؛ المراحل ليست حالة معرفية، والمواد المقفلة لا تظهر قبل تحقق حدود العزل والقفل القائمة."
        actions={
          <>
            <Link className="button button-primary button-small" href={`/run/${run.id}/blind`}>فتح المختبر المعزول</Link>
            <Link className="button button-secondary button-small" href={`/run/${run.id}/knowledge`}>مستكشف المعرفة R1</Link>
          </>
        }
      />

      <div className="context-strip" aria-label="سياق تشغيل البحث">
        <span>Run <b className="technical-text">{run.id}</b></span>
        <span>المنهجية <b className="technical-text">{run.methodology_revision}</b></span>
        <span>Corpus <b className="technical-text">{run.corpus_snapshot}</b></span>
        <span>المرحلة <b className="technical-text">{run.current_stage}</b></span>
        <span>الحالة التشغيلية <b className="technical-text">{run.status}</b></span>
      </div>

      <nav className="tabs" role="tablist" aria-label="أقسام تشغيل البحث">
        {([
          ["overview", "نظرة عامة"],
          ["artifacts", "المواد البحثية"],
          ["gates", "البوابات والنتائج"],
        ] as const).map(([value, label]) => (
          <button key={value} className="tab" role="tab" type="button" aria-selected={view === value} onClick={() => setView(value)}>{label}</button>
        ))}
      </nav>

      {view === "overview" && (
        <>
          <Panel title="التقدم المنهجي" eyebrow="Analysis stage · not epistemic status">
            <div className="progression" aria-label="تسلسل مراحل البحث">
              {stages.map((stage) => <span key={stage} className={run.current_stage === stage ? "active" : undefined}>{stage}</span>)}
            </div>
            <p className="field-error">اكتمال مرحلة أو فحص لا يعني صحة الفرضية ولا يمنح قفلاً معرفياً.</p>
          </Panel>

          <section className="metric-grid" aria-label="جرد المواد المحفوظة">
            <article className="metric-card information"><span>الملاحظات البنيوية</span><strong>{data.observations.length}</strong><small>ObservationArtifact</small></article>
            <article className="metric-card warning"><span>الفرضيات</span><strong>{data.hypotheses.length}</strong><small>H1 / H2 / C0</small></article>
            <article className="metric-card stale"><span>تقارير البوابات</span><strong>{data.gates.length}</strong><small>قائمة ديناميكية من العقد</small></article>
            <article className="metric-card positive"><span>الدعاوى المتاحة</span><strong>{data.claims.length}</strong><small>{data.claims_visible ? "حدود الإتاحة محققة" : "محجوبة قبل الإتاحة"}</small></article>
          </section>

          <Panel title="نقطة الاستئناف الدائمة" eyebrow="Durable checkpoint retrieved">
            <div className="two-column equal-columns">
              <div className="list-card">
                <strong>آخر مرحلة محفوظة</strong>
                <span className="technical-text">{run.current_stage}</span>
                <small>آخر تحديث: {new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(run.updated_at))}</small>
              </div>
              <div className="list-card">
                <strong>الإجراءات المتاحة</strong>
                <span>متابعة المختبر المعزول وقراءة الإسقاط المعرفي المصرح به.</span>
                <small>لا تعتمد الاستعادة على ذاكرة المحادثة.</small>
              </div>
            </div>
          </Panel>
        </>
      )}

      {view === "artifacts" && (
        <div className="two-column equal-columns">
          <Panel title="الملاحظات البنيوية" eyebrow="Observations">
            {data.observations.length === 0 ? <EmptyState title="لا توجد ملاحظات" detail="ابدأ من Blind Lab وسجّل وصفاً بنيوياً دون استنتاج دلالي." /> : (
              <div className="stack">{data.observations.map((item) => (
                <article className="list-card" key={item.id}>
                  <strong>{item.form || "Form غير مسجل"}</strong>
                  <span>{item.syntax || "Syntax غير مسجل"}</span>
                  <small className="technical-text">{item.occurrence_ref} · {item.id}</small>
                </article>
              ))}</div>
            )}
          </Panel>

          <Panel title="مختبر الفرضيات" eyebrow="H1 · H2 · C0">
            {data.hypotheses.length === 0 ? <EmptyState title="لا توجد فرضيات محفوظة" detail="لا تعلن الواجهة فائزاً عند غياب الأدلة." /> : (
              <div className="stack">{data.hypotheses.map((item) => (
                <article className="list-card" key={item.id}>
                  <StatusBadge label="النوع" value={item.hypothesis_type} />
                  <strong>{item.statement}</strong>
                  <span>شرط النقض: {item.rejection_condition.challenging_finding}</span>
                  <small>مؤيدات: {item.supporting_evidence_refs.length} · معارضات: {item.counterevidence_refs.length} · غير محسوم: {item.unresolved_cases.length}</small>
                </article>
              ))}</div>
            )}
          </Panel>
        </div>
      )}

      {view === "gates" && (
        <>
          <Panel title="تقارير بوابات القفل" eyebrow="Dynamic GateReport list">
            {data.gates.length === 0 ? <EmptyState title="لا توجد تقارير بوابات" detail="لن تفترض الواجهة عدداً ثابتاً أو حالة نجاح." /> : (
              <div className="gate-list">{data.gates.map((gate) => (
                <article className="gate-card" key={gate.id}>
                  <div><h3 className="technical-text">{gate.gate_code}</h3><p>Revision: {gate.evaluated_revision}</p></div>
                  <div><StatusBadge label="الحالة" value={gate.status} /><p>{gate.failure_reason || gate.required_action || "لا يوجد سبب أو إجراء إضافي مسجل."}</p></div>
                </article>
              ))}</div>
            )}
          </Panel>

          <Panel title="الدعاوى المرتبطة" eyebrow="Four independent axes">
            {!data.claims_visible && <div className="state-card"><strong>المواد المقفلة غير متاحة</strong><p>الإتاحة تفشل مغلقة حتى يتحقق Internal Lock القائم مع عزل CLEAN. لا تعرض الواجهة prior أو تعريفاً سابقاً.</p></div>}
            {data.claims_visible && data.claims.length === 0 && <EmptyState title="لا توجد دعاوى" detail="اجتياز حدود الإتاحة لا يعني وجود دعوى محفوظة." />}
            <div className="stack">{data.claims.map((claim) => (
              <article className="list-card" key={claim.id}>
                <div className="list-row"><div><strong>{claim.abstract_root_core || claim.root_definition || "دعوى دون نص دلالي مسجل"}</strong><small className="technical-text">{claim.id}</small></div><Link className="button button-secondary button-small" href={`/claims/${claim.id}`}>فتح التتبّع</Link></div>
                <StatusAxes epistemic={claim.epistemic_state} review={claim.review_state} freshness={claim.freshness_state} publication={claim.publication_state} compact />
                <div className="evidence-grid">
                  <div className="evidence-column"><h3>الأدلة المؤيدة</h3><pre>{JSON.stringify(claim.supporting_evidence ?? {}, null, 2)}</pre></div>
                  <div className="evidence-column counter"><h3>الأدلة المعارضة</h3><pre>{JSON.stringify(claim.counterevidence ?? {}, null, 2)}</pre></div>
                </div>
              </article>
            ))}</div>
          </Panel>
        </>
      )}

      <details className="raw-details">
        <summary>التفاصيل التقنية الخام</summary>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </details>
    </main>
  );
}
