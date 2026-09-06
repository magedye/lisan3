"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { StatusBadge } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

type ResearchRun = components["schemas"]["ResearchRunResponse"];
type IsolationState = components["schemas"]["IsolationStateResponse"];
type CorpusOccurrence = components["schemas"]["CorpusOccurrenceResponse"];
type Observation = components["schemas"]["ObservationArtifactResponse"];

export default function BlindLabPage() {
  const params = useParams();
  const runId = params.id as string;
  const [run, setRun] = useState<ResearchRun | null>(null);
  const [isolation, setIsolation] = useState<IsolationState | null>(null);
  const [corpus, setCorpus] = useState<CorpusOccurrence[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [form, setForm] = useState("");
  const [syntax, setSyntax] = useState("");
  const [revision, setRevision] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    async function fetchBlindLab() {
      try {
        const runData = await apiFetch<ResearchRun>(`/api/runs/${runId}`, { signal: controller.signal });
        setRun(runData);
        const isolationResponse = await fetch(`/api/runs/${runId}/blind`, { cache: "no-store", signal: controller.signal });
        if (isolationResponse.status === 404) {
          setIsolation(null);
          setCorpus([]);
          return;
        }
        if (!isolationResponse.ok) throw new Error(`تعذر تحميل حالة العزل: HTTP ${isolationResponse.status}`);
        const isolationData = (await isolationResponse.json()) as IsolationState;
        setIsolation(isolationData);
        if (isolationData.is_contaminated === "CLEAN") {
          setCorpus(await apiFetch<CorpusOccurrence[]>(`/api/runs/${runId}/corpus`, { signal: controller.signal }));
        } else {
          setCorpus([]);
        }
      } catch (reason) {
        if (reason instanceof DOMException && reason.name === "AbortError") return;
        setError(reason instanceof Error ? reason.message : "تعذر تحميل المختبر المعزول.");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void fetchBlindLab();
    return () => controller.abort();
  }, [runId, revision]);

  async function startPreflight() {
    if (!run) return;
    setBusy(true);
    setError(null);
    try {
      await apiFetch<IsolationState>(`/api/runs/${runId}/blind/preflight`, {
        method: "POST",
      });
      setNotice("فعّل المضيف عزل المصدر تلقائياً وسجّل CLEAN. محاولة القراءة المحظورة المرفوضة لا تعني تلوثاً فعلياً.");
      setRevision((value) => value + 1);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر بدء فحص العزل.");
    } finally {
      setBusy(false);
    }
  }

  async function submitObservation(event: React.FormEvent) {
    event.preventDefault();
    if (!corpus[0]) {
      setError("لا يمكن تسجيل ملاحظة دون موضع Corpus فعلي متاح في snapshot هذا التشغيل.");
      return;
    }
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const observation = await apiFetch<Observation>(`/api/runs/${runId}/observations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ occurrence_ref: corpus[0].id, form, syntax }),
      });
      setForm("");
      setSyntax("");
      setNotice(`سُجلت الملاحظة البنيوية ${observation.id} دون استنتاج دلالي.`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر تسجيل الملاحظة.");
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <main className="page-frame"><LoadingState label="جارٍ تحميل حدود Blind Lab…" /></main>;
  if (error && !run) return <main className="page-frame"><ErrorState message={error} retry={() => { setLoading(true); setError(null); setRevision((value) => value + 1); }} /></main>;
  if (!run) return <main className="page-frame"><ErrorState message="Run not found." /></main>;

  return (
    <main className="page-frame">
      <div className="isolation-banner" role="status">
        <div><strong>مختبر معزول — قبل القفل الداخلي</strong><span>التعريفات السابقة وOwner answers والمعاجم والتفاسير غير المقبولة غير متاحة في هذا السياق.</span></div>
        <StatusBadge label="العزل" value={isolation?.is_contaminated ?? "UNKNOWN"} />
      </div>

      <PageHeader
        eyebrow="BLIND-LAB · Epistemic Boundary"
        title={`المختبر المعزول: ${run.target_expression}`}
        description="Corpus → Observations → Structure → Hypotheses. الواجهة تعرض فقط ما تسمح به عقود العزل الحالية."
        actions={<span className="status-badge status-information"><span aria-hidden="true">●</span><span className="technical-text">{runId}</span></span>}
      />

      {error && <ErrorState message={error} />}
      {notice && <div className="panel panel-information" role="status">{notice}</div>}

      {!isolation && (
        <Panel title="فحص العزل مطلوب" eyebrow="Isolation Preflight" className="panel-warning">
          <p>قبل قراءة Corpus أو تسجيل الملاحظات، يجب تثبيت snapshot والمنهجية والمصادر المسموح بها في عقد العزل.</p>
          <div className="context-strip">
            <span>Corpus <b className="technical-text">{run.corpus_snapshot}</b></span>
            <span>المنهجية <b className="technical-text">{run.methodology_revision}</b></span>
            <span>المصدر المسموح <b className="technical-text">QURAN_CORPUS</b></span>
          </div>
          <button type="button" onClick={startPreflight} className="button button-primary" disabled={busy}>بدء فحص العزل — Start Preflight Isolation</button>
        </Panel>
      )}

      {isolation?.is_contaminated === "PRIOR_CONTAMINATED" && (
        <Panel title="تم اكتشاف تلوث فعلي بالمعرفة السابقة" eyebrow="PRIOR_CONTAMINATED" className="panel-danger">
          <p>{isolation.contamination_reason || "لم يسجل سبب إضافي."}</p>
          <p><strong>القفل الداخلي محجوب لهذا التشغيل.</strong> هذا يختلف عن محاولة قراءة محظورة رفضها النظام قبل كشف المحتوى.</p>
        </Panel>
      )}

      {isolation?.is_contaminated === "CLEAN" && (
        <div className="two-column equal-columns">
          <Panel title="Corpus المقبول في التشغيل" eyebrow="Admitted source only">
            {corpus.length === 0 ? (
              <EmptyState title="لا توجد مواضع في snapshot" detail={`لم يعثر العقد على مواضع مرتبطة بالمعرّف ${isolation.corpus_snapshot}.`} />
            ) : (
              <div className="stack">{corpus.map((item) => (
                <article className="list-card" key={item.id}>
                  <div className="list-row"><div><strong>{item.expression}</strong><small className="technical-text">{item.verse_ref}</small></div><StatusBadge label="Corpus" value={item.snapshot_id} /></div>
                  <p className="quran-text">{item.text}</p>
                </article>
              ))}</div>
            )}
          </Panel>

          <Panel title="سجّل ملاحظة بنيوية" eyebrow="No semantic conclusion">
            <p>صف الصيغة والبناء فقط. لا تدخل تعريفاً دلالياً أو نتيجة مأخوذة من prior.</p>
            <form className="form-grid" onSubmit={submitObservation}>
              <label className="form-field">
                <span>الصيغة / Morphology</span>
                <input id="observation-form" name="form" className="input" value={form} onChange={(event) => setForm(event.target.value)} placeholder="e.g. past tense verb, pattern fa'ala" required />
              </label>
              <label className="form-field">
                <span>البناء / Syntax</span>
                <input id="observation-syntax" name="syntax" className="input" value={syntax} onChange={(event) => setSyntax(event.target.value)} placeholder="e.g. transitive, takes direct object" required />
              </label>
              <div className="form-field form-field-full">
                <button className="button button-primary" type="submit" disabled={busy || corpus.length === 0}>حفظ الملاحظة — Save Observation</button>
              </div>
            </form>
            <div className="panel panel-muted">
              <strong>حد العزل</strong>
              <p>القراءة المحظورة تُرفض من backend. رفض المحاولة لا يغيّر الحالة إلى PRIOR_CONTAMINATED؛ التلوث الفعلي له سجل منفصل.</p>
            </div>
          </Panel>
        </div>
      )}
    </main>
  );
}
