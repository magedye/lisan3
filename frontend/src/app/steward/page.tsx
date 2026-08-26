"use client";

import type { components } from "@/api/openapi";
import { ConfirmDialog } from "@/components/confirm-dialog";
import { EmptyState, ErrorState, PageHeader, Panel } from "@/components/page-primitives";
import { StatusBadge } from "@/components/status-axes";
import { apiFetch } from "@/lib/api";
import { useState } from "react";

type StewardCommand = components["schemas"]["StewardCommandResponse"];
type AuditLog = components["schemas"]["AuditLogResponse"];
type CommandDraft = { command_type: string; intent: string; parameters: Record<string, unknown> };

export default function StewardPage() {
  const [commandType, setCommandType] = useState("");
  const [intent, setIntent] = useState("");
  const [parametersText, setParametersText] = useState("{}");
  const [preview, setPreview] = useState<CommandDraft | null>(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [result, setResult] = useState<StewardCommand | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [busy, setBusy] = useState(false);

  function buildPreview(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    setResult(null);
    try {
      const parsed: unknown = JSON.parse(parametersText);
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("يجب أن تكون parameters كائن JSON.");
      setPreview({ command_type: commandType.trim(), intent: intent.trim(), parameters: parsed as Record<string, unknown> });
    } catch (reason) {
      setPreview(null);
      setError(reason instanceof Error ? reason.message : "JSON غير صالح.");
    }
  }

  async function executeCommand() {
    if (!preview) return;
    setBusy(true);
    setError(null);
    try {
      const response = await apiFetch<StewardCommand>("/api/steward/commands", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(preview),
      });
      setResult(response);
      setConfirmOpen(false);
      setPreview(null);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر تنفيذ الأمر.");
      setConfirmOpen(false);
    } finally {
      setBusy(false);
    }
  }

  async function fetchLogs(commandId: string) {
    setBusy(true);
    setError(null);
    try {
      setAuditLogs(await apiFetch<AuditLog[]>(`/api/audit?entity_type=StewardCommand&entity_id=${encodeURIComponent(commandId)}`));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "تعذر تحميل سجل الأمر.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="STEWARD · Governed Command"
        title="مركز أوامر Steward — Steward Command Center"
        description="User intent → Preview → Backend validation → Execute → Audit. لا يستطيع Steward إنشاء حقيقة دلالية أو تجاوز Gate."
        actions={<StatusBadge label="الحد" value="NO_DIRECT_CANONICAL_WRITE" />}
      />

      {error && <div id="cmd-error"><ErrorState message={error} /></div>}

      <div className="two-column">
        <Panel title="صياغة النية" eyebrow="Step 1 · Input">
          <form className="form-grid" onSubmit={buildPreview}>
            <label className="form-field">
              <span>Command Type</span>
              <input id="steward-command-type" name="command_type" className="input technical-text" value={commandType} onChange={(event) => setCommandType(event.target.value)} placeholder="نوع أمر مدعوم" required />
              <small>لا توجد أوامر تنفيذية محكومة مسجلة حالياً؛ يعيد backend حالة UNSUPPORTED أو REJECTED بصراحة.</small>
            </label>
            <label className="form-field">
              <span>النية</span>
              <textarea id="steward-intent" name="intent" className="textarea" value={intent} onChange={(event) => setIntent(event.target.value)} placeholder="صف التغيير أو الطلب دون ادعاء سلطة" required />
            </label>
            <label className="form-field form-field-full">
              <span>Parameters (JSON)</span>
              <textarea id="steward-parameters" name="parameters" className="textarea technical-text" dir="ltr" value={parametersText} onChange={(event) => setParametersText(event.target.value)} aria-describedby="parameters-help" />
              <small id="parameters-help">لا تضع أسراراً أو بيانات غير لازمة في المعلمات.</small>
            </label>
            <div className="form-field form-field-full"><button className="button button-primary" type="submit">Preview Governed Command — معاينة الأمر</button></div>
          </form>
        </Panel>

        <Panel title="معاينة الأثر والسلطة" eyebrow="Step 2 · Preview">
          {!preview ? <EmptyState title="لا توجد معاينة" detail="أدخل النية والمعلمات ثم أنشئ معاينة قبل التنفيذ." /> : (
            <div className="stack">
              <div className="list-card"><strong>الأمر</strong><span className="technical-text">{preview.command_type}</span></div>
              <div className="list-card"><strong>النية</strong><span>{preview.intent}</span></div>
              <div className="list-card"><strong>حد السلطة</strong><span>التحقق والتنفيذ في backend؛ لا كتابة مباشرة في canonical semantic knowledge.</span></div>
              <div className="list-card"><strong>الأثر المتوقع</strong><span>يسجل backend النتيجة الفعلية فقط عند قبول الأمر.</span><small>الأثر التفصيلي غير متاح كعقد preview مستقل.</small></div>
              <details className="raw-details"><summary>المعلمات الخام</summary><pre>{JSON.stringify(preview.parameters, null, 2)}</pre></details>
              <button className="button button-secondary" type="button" onClick={() => setConfirmOpen(true)}>مراجعة التأكيد — Execute Command</button>
            </div>
          )}
        </Panel>
      </div>

      {result && (
        <Panel title="نتيجة التنفيذ" eyebrow="Backend result">
          <div className="list-row">
            <div><span id="cmd-status"><StatusBadge label="Status" value={result.execution_status} /></span><strong>{result.result_summary || "لا ملخص مسجل"}</strong><small className="technical-text">{result.id}</small></div>
            <button className="button button-quiet button-small" type="button" onClick={() => void fetchLogs(result.id)} disabled={busy}>View Audit Logs — سجل الأمر</button>
          </div>
          <details className="raw-details"><summary>القواعد التي قيّمها backend</summary><pre>{JSON.stringify(result.evaluated_rules ?? {}, null, 2)}</pre></details>
        </Panel>
      )}

      {result && (
        <Panel title="سجل التدقيق المرتبط" eyebrow="Audit linkage">
          {auditLogs.length === 0 ? <EmptyState title="لم يُطلب السجل أو لا توجد أحداث" detail="استخدم زر سجل الأمر لقراءة AuditLog الفعلي." /> : (
            <div className="table-wrap" id="audit-logs-section"><table><thead><tr><th>الوقت</th><th>الفاعل</th><th>الإجراء</th><th>الحالة</th></tr></thead><tbody>{auditLogs.map((log) => (
              <tr className="audit-log" key={log.id}><td>{new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(log.created_at))}</td><td className="log-actor">{log.actor}</td><td className="log-action">{log.action}</td><td>{log.new_state ?? "—"}</td></tr>
            ))}</tbody></table></div>
          )}
        </Panel>
      )}

      <ConfirmDialog
        open={confirmOpen}
        title="تأكيد تنفيذ أمر Steward"
        description="سيُرسل الأمر المعروض إلى backend للتحقق. قد يُرفض إذا تجاوز حدود السلطة أو العقد، ولا يعني التأكيد أن الأثر مسموح."
        confirmLabel="إرسال للتحقق والتنفيذ"
        danger
        busy={busy}
        onConfirm={() => void executeCommand()}
        onClose={() => setConfirmOpen(false)}
      />
    </main>
  );
}
