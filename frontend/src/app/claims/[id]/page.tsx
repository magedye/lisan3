"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { ResearchStatus, StatusBadge } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

type Claim = components["schemas"]["SemanticClaimResponse"];
type Diagnostics = components["schemas"]["MethodologyDiagnosticsResponse"];
type Manifest = components["schemas"]["ReproductionManifestResponse"];
type History = components["schemas"]["ClaimHistoryResponse"];
type Provenance = {
  claim: { id: string; contract_type: string; research_state: string; canonical_state: string };
  dependencies: Array<{ type: string; ref: string; rev: number | null }>;
  research_run: { id: string; methodology_revision: string } | null;
  corpus_snapshot: string | null;
  audit_trail: Array<{ action: string; actor: string; new_state: string | null; timestamp: string }>;
};
type ClaimBundle = { claim: Claim; diagnostics: Diagnostics; manifest: Manifest; history: History; provenance: Provenance };

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
        const claim = await apiFetch<Claim>(`/api/judgments/${claimId}`, {
          signal: controller.signal,
        });
        const provenance = await apiFetch<Provenance>(
          `/api/judgments/${claimId}/provenance`,
          { signal: controller.signal },
        );
        const diagnostics = await apiFetch<Diagnostics>(`/api/judgments/${claimId}/diagnostics`, {
          signal: controller.signal,
        });
        const manifest = await apiFetch<Manifest>(
          `/api/judgments/${claimId}/reproduction-manifest`,
          { signal: controller.signal },
        );
        const history = await apiFetch<History>(`/api/judgments/${claimId}/history`, {
          signal: controller.signal,
        });
        setBundle({ claim, provenance, diagnostics, manifest, history });
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

  const { claim, provenance, diagnostics, manifest, history } = bundle;
  const claimText = claim.preferred_conclusion || claim.root_concept;

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="CLAIM TRACEABILITY · Governed Read Model"
        title={claimText || "دعوى دلالية دون نص مسجل"}
        description={`العقد: ${claim.contract_type}. يُعرض حكم البحث منفصلاً عن الاعتماد، مع الدليل والمعارضات والمصدر.`}
        actions={<span className="status-badge status-information"><span aria-hidden="true">●</span><span className="technical-text">{claim.id}</span></span>}
      />

      <ResearchStatus research={claim.research_state} canonical={claim.canonical_state} strength={claim.result_strength} verification={claim.verification_state} />

      {claim.canonical_state === "REOPEN_REQUIRED" && (
        <div className="panel panel-warning" role="alert">
          <strong>هذه النتيجة تحتاج إعادة فتح البحث.</strong>
          <p>لا تُسترجع كنتيجة معتمدة حتى معالجة الدليل الجديد والتحقق من النسخة الحالية.</p>
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

        <Panel title="التشخيصات المنهجية" eyebrow="Diagnostics · not research gates">
          <div className="button-row">
            <span id="qual-findings" className="status-badge status-neutral"><span aria-hidden="true">●</span>{diagnostics.findings.length} findings</span>
            <StatusBadge label="Hard blockers" value={diagnostics.hard_blockers.length ? "FAILED" : "CLEAN"} />
          </div>
          <p>غياب extractor يظهر `NOT_EVALUATED` ولا يتحول إلى بوابة فشل عامة.</p>
          <div className="stack">{diagnostics.findings.map((finding) => (
            <article className="list-card" key={finding.dimension}>
              <div className="list-row"><div><strong className="technical-text">{finding.dimension}</strong><span>{finding.details}</span></div><StatusBadge label={finding.severity} value={finding.status} /></div>
            </article>
          ))}</div>
        </Panel>
      </div>

      <Panel title="التاريخ والتحقق" eyebrow={`Revision ${history.current_revision}`}>
        {history.verification_records.length === 0 && history.audit_events.length === 0 ? (
          <EmptyState title="لا يوجد تاريخ تحقق أو تدقيق" detail="تعرض الواجهة السجل الفعلي فقط." />
        ) : (
          <div className="two-column equal-columns">
            <div>
              <h3>سجلات التحقق</h3>
              <div className="stack">{history.verification_records.map((verification) => (
                <article className="list-card" key={verification.id}><StatusBadge label="القرار" value={verification.decision} /><strong>{verification.verifier_identity}</strong><span>{verification.rationale || "لا توجد حيثيات مسجلة"}</span><small>Revision {verification.evaluated_claim_revision}</small></article>
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
