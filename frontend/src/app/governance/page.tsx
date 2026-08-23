"use client";

import { useState } from "react";

export default function GovernancePage() {
  const [ruleCode, setRuleCode] = useState("RULE_E2E_ROOT");
  const [proposedChanges, setProposedChanges] = useState("");
  const [proposalId, setProposalId] = useState("");
  const [history, setHistory] = useState<any>(null);

  const submitProposal = async () => {
    const res = await fetch("/api/governance/proposals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rule_code: ruleCode, proposed_changes: proposedChanges })
    });
    if (res.ok) {
      const data = await res.json();
      setProposalId(data.id);
    }
  };

  const approveProposal = async () => {
    await fetch(`/api/governance/proposals/${proposalId}/approve`, { method: "POST" });
  };

  const checkHistory = async () => {
    const res = await fetch(`/api/governance/rules/${ruleCode}/history`);
    if (res.ok) {
      setHistory(await res.json());
    }
  };

  return (
    <div className="p-8">
      <h1>Governance Center</h1>

      <div>
        <input value={ruleCode} onChange={(e) => setRuleCode(e.target.value)} placeholder="Rule Code" />
        <textarea value={proposedChanges} onChange={(e) => setProposedChanges(e.target.value)} placeholder="Proposed changes" />
        <button onClick={submitProposal}>Submit Proposal</button>
      </div>

      {proposalId && (
        <div>
          <span>Proposal ID: {proposalId}</span>
          <button onClick={approveProposal}>Approve Proposal</button>
        </div>
      )}

      <div>
        <button onClick={checkHistory}>Check History</button>
        {history && (
          <div>
            <span id="active-revision">Revision: {history.active_revision}</span>
            <span id="revisions-count">Revisions: {history.revisions?.length || 0}</span>
          </div>
        )}
      </div>
    </div>
  );
}
