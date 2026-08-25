"use client";

import type { components } from "@/api/openapi";
import { useEffect, useState } from "react";

type AuditLog = components["schemas"]["AuditLogResponse"];

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadAudit() {
      try {
        const response = await fetch("/api/audit?limit=100", {
          signal: controller.signal,
          cache: "no-store",
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        setLogs((await response.json()) as AuditLog[]);
      } catch (caught) {
        if (caught instanceof DOMException && caught.name === "AbortError") return;
        setError("تعذّر تحميل سجل التدقيق من الخدمة الخلفية.");
      } finally {
        setLoading(false);
      }
    }

    void loadAudit();
    return () => controller.abort();
  }, []);

  return (
    <main className="page-frame">
      <section className="page-heading">
        <div>
          <span className="eyebrow">Golden UX · Audit Log</span>
          <h1>سجل التدقيق</h1>
          <p>سجل قراءة فقط للأحداث التي كتبها النظام عبر العقود الخلفية الفعلية.</p>
        </div>
        <span className="truth-badge">قراءة فقط</span>
      </section>

      <section className="audit-panel" aria-live="polite">
        {loading && <p className="empty-state">جارٍ تحميل السجل…</p>}
        {error && <p className="empty-state error-panel" role="alert">{error}</p>}
        {!loading && !error && logs.length === 0 && (
          <div className="empty-state">
            <strong>لا توجد أحداث تدقيق مسجلة</strong>
            <span>لم تُنشئ الواجهة سجلات تجريبية لملء هذا العرض.</span>
          </div>
        )}
        {!loading && !error && logs.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>الوقت</th>
                  <th>الكيان</th>
                  <th>الإجراء</th>
                  <th>الفاعل</th>
                  <th>الحالة الجديدة</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>{new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(log.created_at))}</td>
                    <td><strong>{log.entity_type}</strong><small>{log.entity_id}</small></td>
                    <td><span className="table-chip">{log.action}</span></td>
                    <td>{log.actor}</td>
                    <td>{log.new_state ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}
