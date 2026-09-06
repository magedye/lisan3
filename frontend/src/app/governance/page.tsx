"use client";

import type { components } from "@/api/openapi";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { ResearchStatus, StatusBadge } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import { useApiResource } from "@/lib/use-api-resource";
import Link from "next/link";
import { useState } from "react";

type Overview = components["schemas"]["GovernanceOverviewResponse"];
type RuleHistory = components["schemas"]["RuleHistoryResponse"];
type Proposal = components["schemas"]["ChangeProposalResponse"];
type Rule = components["schemas"]["GovernanceRuleResponse"];
type Tab = "rules" | "review" | "sources";

export default function GovernancePage() {
  const overview = useApiResource<Overview>("/api/governance/overview");
  const [tab, setTab] = useState<Tab>("rules");
  const [ruleCode, setRuleCode] = useState("");
  const [ruleDescription, setRuleDescription] = useState("");
  const [proposedChanges, setProposedChanges] = useState("");
  const [proposalId, setProposalId] = useState("");
  const [history, setHistory] = useState<RuleHistory | null>(null);
  const [pendingApproval, setPendingApproval] = useState<Proposal | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  async function createRule(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const rule = await apiFetch<Rule>("/api/governance/rules", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rule_code: ruleCode, description: ruleDescription }),
      });
      setNotice(`أُنشئت القاعدة ${rule.rule_code} مع revision ${rule.active_revision}.`);
      setRuleDescription("");
      overview.reload();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر إنشاء القاعدة.");
    } finally {
      setBusy(false);
    }
  }

  async function submitProposal(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const proposal = await apiFetch<Proposal>("/api/governance/proposals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rule_code: ruleCode, proposed_changes: proposedChanges }),
      });
      setProposalId(proposal.id);
      setNotice(`Proposal ID: ${proposal.id}`);
      setProposedChanges("");
      overview.reload();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر إنشاء مقترح التغيير.");
    } finally {
      setBusy(false);
    }
  }

  async function approveProposal() {
    if (!pendingApproval) return;
    setBusy(true);
    setError(null);
    try {
      const proposal = await apiFetch<Proposal>(`/api/governance/proposals/${pendingApproval.id}/approve`, { method: "POST" });
      setPendingApproval(null);
      setNotice(`اعتمد المقترح ${proposal.id}. راجع التاريخ وأثر الإبطال المتعدي.`);
      overview.reload();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر اعتماد المقترح.");
    } finally {
      setBusy(false);
    }
  }

  async function checkHistory(code = ruleCode) {
    if (!code.trim()) {
      setError("أدخل رمز قاعدة موجودة لقراءة تاريخها.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      setHistory(await apiFetch<RuleHistory>(`/api/governance/rules/${encodeURIComponent(code.trim())}/history`));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر تحميل تاريخ القاعدة.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="GOVERNANCE CENTER · Current contracts"
        title="مركز الحوكمة — Governance Center"
        description="القواعد والمقترحات ومرشحات الاعتماد وقبول المصادر من الحالة المحفوظة. البحث لا ينتظر مسار مراجعة إداري."
        actions={<StatusBadge label="المسار" value="CHANGE_PROPOSAL_REQUIRED" />}
      />

      <nav className="tabs" role="tablist" aria-label="أقسام مركز الحوكمة">
        <button className="tab" role="tab" type="button" aria-selected={tab === "rules"} onClick={() => setTab("rules")}>القواعد والمقترحات</button>
        <button className="tab" role="tab" type="button" aria-selected={tab === "review"} onClick={() => setTab("review")}>مرشحات الاعتماد</button>
        <button className="tab" role="tab" type="button" aria-selected={tab === "sources"} onClick={() => setTab("sources")}>المصادر والقبول</button>
      </nav>

      {error && <ErrorState message={error} />}
      {notice && <div className="panel panel-information" role="status">{notice}</div>}
      {overview.loading && <LoadingState label="جارٍ تحميل الحوكمة والمراجعة…" />}
      {overview.error && <ErrorState message={overview.error} retry={overview.reload} />}

      {tab === "rules" && overview.data && (
        <>
          <section className="metric-grid">
            <article className="metric-card information"><span>القواعد</span><strong>{overview.data.rules.length}</strong><small>GovernanceRule</small></article>
            <article className="metric-card warning"><span>المقترحات المفتوحة</span><strong>{overview.data.proposals.filter((item) => item.status === "PROPOSED").length}</strong><small>تحتاج قراراً صريحاً</small></article>
            <article className="metric-card stale"><span>تحتاج إعادة فتح</span><strong>{overview.data.reopen_required.length}</strong><small>REOPEN_REQUIRED</small></article>
            <article className="metric-card positive"><span>مرشحة للاعتماد</span><strong>{overview.data.canonicalization_candidates.length}</strong><small>تحقق مستقل ثم قرار Host</small></article>
          </section>

          <div className="two-column">
            <Panel title="مستودع القواعد" eyebrow="Active revisions">
              {overview.data.rules.length === 0 ? <EmptyState title="لا توجد قواعد مسجلة" detail="يمكن إنشاء قاعدة أولية من العقد المخصص أدناه." /> : (
                <div className="stack">{overview.data.rules.map((rule) => (
                  <button type="button" className="list-card" key={rule.id} onClick={() => { setRuleCode(rule.rule_code); void checkHistory(rule.rule_code); }}>
                    <strong className="technical-text">{rule.rule_code}</strong><span>{rule.description}</span><small>Active revision: {rule.active_revision}</small>
                  </button>
                ))}</div>
              )}
            </Panel>

            <Panel title="تاريخ القاعدة" eyebrow="Immutable revisions">
              {!history ? <EmptyState title="اختر قاعدة" detail="افتح قاعدة من المستودع أو أدخل رمزها ثم اضغط Check History." /> : (
                <div>
                  <div className="context-strip"><span>Rule <b className="technical-text">{history.rule_code}</b></span><span id="active-revision">Revision: {history.active_revision}</span><span id="revisions-count">Revisions: {history.revisions.length}</span></div>
                  <div className="stack">{history.revisions.map((revision) => (
                    <article className="list-card" key={revision.id}><strong>Revision {revision.revision_number}</strong><span>{revision.changes_described || "لا وصف مسجل"}</span><small>{revision.approved_by || "لا معتمد مسجل"}</small></article>
                  ))}</div>
                </div>
              )}
            </Panel>
          </div>

          <div className="two-column equal-columns">
            <Panel title="إنشاء قاعدة أولية" eyebrow="GovernanceRuleCreate">
              <form className="form-grid" onSubmit={createRule}>
                <label className="form-field"><span>Rule Code</span><input id="new-rule-code" name="rule_code" className="input technical-text" value={ruleCode} onChange={(event) => setRuleCode(event.target.value)} placeholder="Rule Code" required /></label>
                <label className="form-field"><span>الوصف</span><input id="new-rule-description" name="description" className="input" value={ruleDescription} onChange={(event) => setRuleDescription(event.target.value)} placeholder="وصف القاعدة" required /></label>
                <div className="form-field form-field-full"><button className="button button-primary" type="submit" disabled={busy}>إنشاء القاعدة</button></div>
              </form>
            </Panel>

            <Panel title="مقترح تغيير" eyebrow="Impact preview before approval">
              <form className="form-grid" onSubmit={submitProposal}>
                <label className="form-field"><span>Rule Code</span><input id="proposal-rule-code" name="rule_code" className="input technical-text" value={ruleCode} onChange={(event) => setRuleCode(event.target.value)} placeholder="Rule Code" required /></label>
                <label className="form-field"><span>التغيير المقترح</span><textarea id="proposed-changes" name="proposed_changes" className="textarea" value={proposedChanges} onChange={(event) => setProposedChanges(event.target.value)} placeholder="Proposed changes" required /></label>
                <div className="form-field form-field-full button-row"><button className="button button-secondary" type="submit" disabled={busy}>Submit Proposal — إرسال المقترح</button><button className="button button-quiet" type="button" onClick={() => void checkHistory()} disabled={busy}>Check History — قراءة التاريخ</button></div>
              </form>
            </Panel>
          </div>

          <Panel title="المقترحات وتحليل الأثر" eyebrow="No implicit approval">
            {overview.data.proposals.length === 0 ? <EmptyState title="لا توجد مقترحات" detail="لن تعرض الواجهة قرارات تجريبية." /> : (
              <div className="table-wrap"><table><thead><tr><th>المقترح</th><th>القاعدة</th><th>الأثر المحسوب</th><th>الحالة</th><th>الإجراء</th></tr></thead><tbody>{overview.data.proposals.map((proposal) => (
                <tr key={proposal.id}><td><strong>{proposal.proposed_changes}</strong><small className="technical-text">{proposal.id}</small></td><td className="technical-text">{proposal.rule_code}</td><td className="technical-text">{JSON.stringify(proposal.impact_analysis)}</td><td><StatusBadge label="الحالة" value={proposal.status} /></td><td>{proposal.status === "PROPOSED" ? <button className="button button-primary button-small" type="button" onClick={() => setPendingApproval(proposal)}>Approve Proposal — مراجعة الاعتماد</button> : "—"}</td></tr>
              ))}</tbody></table></div>
            )}
            {proposalId && <span className="technical-text">Proposal ID: {proposalId}</span>}
          </Panel>
        </>
      )}

      {tab === "review" && overview.data && (
        <Panel title="مرشحات الاعتماد" eyebrow="Research Judgment → Verification → Canonicalization">
          {overview.data.canonicalization_candidates.length === 0 ? <EmptyState title="لا توجد مرشحات" detail="لا توجد نتائج قوية مفضلة تنتظر الاعتماد." /> : (
            <div className="stack">{overview.data.canonicalization_candidates.map((claim) => (
              <article className="list-card" key={claim.id}><div className="list-row"><div><strong>{claim.preferred_conclusion || claim.root_concept || claim.contract_type}</strong><small className="technical-text">{claim.id}</small></div><Link className="button button-secondary button-small" href={`/claims/${claim.id}`}>فتح الحكم</Link></div><ResearchStatus research={claim.research_state} canonical={claim.canonical_state} compact /></article>
            ))}</div>
          )}
        </Panel>
      )}

      {tab === "sources" && overview.data && (
        <Panel title="المصادر والقبول" eyebrow="Corpus authority axes">
          {overview.data.corpus_snapshots.length === 0 ? <EmptyState title="لا توجد Corpus Snapshots" detail="لن تفترض الواجهة قبول مصدر غير مسجل." /> : (
            <div className="table-wrap"><table><thead><tr><th>المصدر</th><th>دور المصدر</th><th>وجود الأثر</th><th>التحقق من البصمة</th><th>التفعيل</th></tr></thead><tbody>{overview.data.corpus_snapshots.map((snapshot) => (
              <tr key={snapshot.id}><td><strong>{snapshot.canonical_text_source}</strong><small className="technical-text">{snapshot.id} · {snapshot.canonical_text_version}</small></td><td><StatusBadge label="الدور" value={snapshot.source_role_status} /></td><td><StatusBadge label="الأثر" value={snapshot.artifact_presence_status} /></td><td><StatusBadge label="البصمة" value={snapshot.hash_verification_status} /></td><td><StatusBadge label="التفعيل" value={snapshot.activation_status} />{snapshot.fixture_only && <small>FIXTURE_ONLY</small>}</td></tr>
            ))}</tbody></table></div>
          )}
        </Panel>
      )}

      <ConfirmDialog
        open={Boolean(pendingApproval)}
        title="اعتماد revision جديد"
        description={pendingApproval ? `سيُعتمد المقترح ${pendingApproval.id} وتُطبّق سياسة الإبطال المتعدي القائمة. لا يمكن للواجهة التراجع عن هذا الأثر تلقائياً.` : ""}
        confirmLabel="تأكيد الاعتماد"
        danger
        busy={busy}
        onConfirm={() => void approveProposal()}
        onClose={() => setPendingApproval(null)}
      />
    </main>
  );
}
