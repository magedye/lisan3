"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { StatusAxes, StatusBadge } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

type Claim = components["schemas"]["SemanticClaimResponse"];
type Quality = components["schemas"]["QualityProfileResponse"];
type Manifest = components["schemas"]["ReproductionManifestResponse"];
type History = components["schemas"]["ClaimHistoryResponse"];
type Provenance = {
  claim: { id: string; contract_type: string; epistemic_state: string };
  dependencies: Array<{ type: string; ref: string; rev: number | null }>;
  research_run: { id: string; methodology_revision: string } | null;
  corpus_snapshot: string | null;
  audit_trail: Array<{ action: string; actor: string; new_state: string | null; timestamp: string }>;
};
type ClaimBundle = { claim: Claim; quality: Quality; manifest: Manifest; history: History; provenance: Provenance };

export default function ClaimPage() {
  const params = useParams();
  const claimId = params.id as string;
  const [bundle, setBundle] = useState<ClaimBundle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    async function fetchClaimBundle() {
      try {
        // Establish claim visibility first. The dependent reads must never race
        // ahead of the Blind Lab release boundary enforced by this contract.
        const claim = await apiFetch<Claim>(`/api/claims/${claimId}`, {
          signal: controller.signal,
        });
        const provenance = await apiFetch<Provenance>(
          `/api/claims/${claimId}/provenance`,
          { signal: controller.signal },
        );
        const quality = await apiFetch<Quality>(`/api/claims/${claimId}/quality`, {
          signal: controller.signal,
        });
        const manifest = await apiFetch<Manifest>(
          `/api/claims/${claimId}/reproduction_manifest`,
          { signal: controller.signal },
        );
        const history = await apiFetch<History>(`/api/claims/${claimId}/history`, {
          signal: controller.signal,
        });
        setBundle({ claim, provenance, quality, manifest, history });
      } catch (reason) {
        if (reason instanceof DOMException && reason.name === "AbortError") return;
        setError(reason instanceof Error ? reason.message : "تعذر تحميل تتبع الدعوى.");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void fetchClaimBundle();
    return () => controller.abort();
  }, [claimId, revision]);

  if (loading) return <main className="page-frame"><LoadingState label="جارٍ بناء سلسلة تتبّع الدعوى…" /></main>;
  if (error || !bundle) return <main className="page-frame"><ErrorState message={error ?? "Claim not found."} retry={() => { setLoading(true); setError(null); setRevision((value) => value + 1); }} /></main>;

  const { claim, provenance, quality, manifest, history } = bundle;
  const claimText = claim.abstract_root_core || claim.root_definition || claim.root_meaning || claim.root_concept;

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="CLAIM TRACEABILITY · Governed Read Model"
        title={claimText || "دعوى دلالية دون نص مسجل"}
        description={`العقد: ${claim.contract_type}. تُعرض الحالة والدليل والمعارضات والمراجعة والمصدر دون استكمال معنى مفقود.`}
        actions={<span className="status-badge status-information"><span aria-hidden="true">●</span><span className="technical-text">{claim.id}</span></span>}
      />

      <StatusAxes epistemic={claim.epistemic_state} review={claim.review_state} freshness={claim.freshness_state} publication={claim.publication_state} />

      {claim.freshness_state !== "CURRENT" && (
        <div className="panel panel-warning" role="alert">
          <strong>هذه الدعوى ليست CURRENT.</strong>
          <p>لا تُعرض كحقيقة حالية؛ راجع سجل الإبطال والمراجعات قبل أي استخدام.</p>
        </div>
      )}

      <div className="two-column equal-columns">
        <Panel title="الأدلة المؤيدة" eyebrow="Evidence">
          {claim.supporting_evidence ? <pre className="technical-text">{JSON.stringify(claim.supporting_evidence, null, 2)}</pre> : <EmptyState title="لا توجد أدلة مؤيدة مسجلة" detail="لا تستنتج الواجهة دليلاً من نص الدعوى." />}
        </Panel>
        <Panel title="الأدلة المعارضة" eyebrow="Counterevidence">
          {claim.counterevidence ? <pre className="technical-text">{JSON.stringify(claim.counterevidence, null, 2)}</pre> : <EmptyState title="لا توجد أدلة معارضة مسجلة" detail="غياب السجل لا يساوي نجاح البحث عن counterevidence." />}
        </Panel>
      </div>

      <div className="two-column">
        <Panel title="المصدر وقابلية إعادة الإنتاج" eyebrow="Provenance chain">
          <div className="stack">
            <div className="list-card"><strong>تشغيل البحث</strong>{provenance.research_run ? <Link className="text-link technical-text" href={`/run/${provenance.research_run.id}`}>{provenance.research_run.id}</Link> : <span>غير مسجل</span>}<small>{provenance.research_run?.methodology_revision ?? "لا مرجع منهجية"}</small></div>
            <div className="list-card"><strong>Corpus Snapshot</strong><span id="prov-corpus" className="technical-text">{provenance.corpus_snapshot ?? "غير مسجل"}</span></div>
            <div className="list-card"><strong>التبعيات</strong><span id="prov-deps">{provenance.dependencies.length} dependencies</span>{provenance.dependencies.map((dep, index) => <small className="technical-text" key={`${dep.type}-${dep.ref}-${index}`}>{dep.type}: {dep.ref} @ {dep.rev ?? "—"}</small>)}</div>
            <div className="list-card"><strong>Manifest</strong><span id="man-corpus" className="technical-text">{manifest.methodology_revision ?? "—"} · {manifest.corpus_snapshot_id ?? "—"}</span><small id="man-deps">{manifest.dependencies.length} dependencies</small></div>
          </div>
        </Panel>

        <Panel title="النقاء المنهجي" eyebrow="Eight dimensions · separate from quality">
          <div className="button-row">
            <span id="quality-availability"><StatusBadge label="QualityProfile" value={quality.available ? "AVAILABLE" : "UNAVAILABLE"} /></span>
            <span id="qual-rating"><StatusBadge label="التقييم" value={quality.purity_rating} /></span>
            <span id="qual-findings" className="status-badge status-neutral"><span aria-hidden="true">●</span>{quality.purity_findings.length} findings</span>
          </div>
          {!quality.available && <div className="state-card" role="status"><strong>QualityProfile unavailable — لم يُقيّم ملف الجودة</strong><p>المعروض أدناه اشتقاق حتمي للنقاء المنهجي فقط؛ المقاييس الأخرى غير متاحة ولا تُستكمل بقيم افتراضية.</p></div>}
          <p>{quality.evaluation_summary}</p>
          <div className="stack">{quality.purity_findings.map((finding) => (
            <article className="list-card" key={finding.dimension}>
              <div className="list-row"><div><strong className="technical-text">{finding.dimension}</strong><span>{finding.details}</span></div><StatusBadge label={finding.severity} value={finding.status} /></div>
            </article>
          ))}</div>
        </Panel>
      </div>

      <Panel title="التاريخ والمراجعة" eyebrow={`Revision ${history.current_revision}`}>
        {history.review_decisions.length === 0 && history.audit_events.length === 0 ? (
          <EmptyState title="لا يوجد تاريخ مراجعة أو تدقيق" detail="تعرض الواجهة السجل الفعلي فقط." />
        ) : (
          <div className="two-column equal-columns">
            <div>
              <h3>قرارات المراجعة</h3>
              <div className="stack">{history.review_decisions.map((review) => (
                <article className="list-card" key={review.id}><StatusBadge label="القرار" value={review.decision} /><strong>{review.reviewer_identity}</strong><span>{review.rationale || "لا توجد حيثيات مسجلة"}</span><small>Revision {review.evaluated_claim_revision}</small></article>
              ))}</div>
            </div>
            <div>
              <h3>أحداث التدقيق</h3>
              <div className="stack" id="prov-audit">{history.audit_events.map((event) => (
                <article className="list-card" key={event.id}><strong>{event.action}</strong><span>{event.actor}</span><small>{new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(event.created_at))}</small></article>
              ))}</div>
            </div>
          </div>
        )}
      </Panel>

      <details className="raw-details">
        <summary>تفاصيل تقنية: claim / provenance / manifest</summary>
        <pre>{JSON.stringify({ claim, provenance, manifest }, null, 2)}</pre>
      </details>
    </main>
  );
}
