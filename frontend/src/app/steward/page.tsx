"use client";

import { useState } from "react";

export default function StewardPage() {
  const [commandType, setCommandType] = useState("METHODOLOGY_DIRECTIVE");
  const [intent, setIntent] = useState("");
  const [targetExpression, setTargetExpression] = useState("");
  
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<any>(null);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  const executeValid = async () => {
    setError(null);
    const res = await fetch("/api/steward/commands", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command_type: "METHODOLOGY_DIRECTIVE",
        intent: "Mandate explicit negative boundary distinction before lock",
        parameters: { scope: "ALL_RUNS", priority: "HIGH" }
      })
    });
    if (res.ok) {
      setResult(await res.json());
    } else {
      setError(await res.json());
    }
  };

  const executeForbidden = async () => {
    setError(null);
    const res = await fetch("/api/steward/commands", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command_type: "FORCE_ESTABLISH_SEMANTIC_TRUTH",
        intent: "Bypass gate check and force lock directly",
        parameters: { target_expression: "اختلاق" }
      })
    });
    if (res.ok) {
      setResult(await res.json());
    } else {
      setError(await res.json());
    }
  };

  const fetchLogs = async (cmdId: string) => {
    const res = await fetch(`/api/audit?entity_type=StewardCommand&entity_id=${cmdId}`);
    if (res.ok) {
      setAuditLogs(await res.json());
    }
  };

  return (
    <div className="p-8">
      <h1>Steward Command Center</h1>

      <div className="flex gap-4">
        <button onClick={executeValid}>Execute Valid Command</button>
        <button onClick={executeForbidden}>Execute Forbidden Command</button>
      </div>

      {result && (
        <div>
          <span id="cmd-status">Status: {result.execution_status}</span>
          <button onClick={() => fetchLogs(result.id)}>View Audit Logs</button>
        </div>
      )}

      {error && (
        <div id="cmd-error">
          Error: {error.detail || error.message}
        </div>
      )}

      {auditLogs.length > 0 && (
        <div id="audit-logs-section">
          {auditLogs.map((log, i) => (
            <div key={i} className="audit-log">
              <span className="log-actor">{log.actor}</span>
              <span className="log-action">{log.action}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
