"use client";

import type { components } from "@/api/openapi";
import { useState } from "react";

type StewardCommand = components["schemas"]["StewardCommandResponse"];
type AuditLog = components["schemas"]["AuditLogResponse"];
type CommandError = { detail?: string; message?: string };

export default function StewardPage() {
  const [result, setResult] = useState<StewardCommand | null>(null);
  const [error, setError] = useState<CommandError | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);

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
      setResult((await res.json()) as StewardCommand);
    } else {
      setError((await res.json()) as CommandError);
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
      setResult((await res.json()) as StewardCommand);
    } else {
      setError((await res.json()) as CommandError);
    }
  };

  const fetchLogs = async (cmdId: string) => {
    const res = await fetch(`/api/audit?entity_type=StewardCommand&entity_id=${cmdId}`);
    if (res.ok) {
      setAuditLogs((await res.json()) as AuditLog[]);
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
