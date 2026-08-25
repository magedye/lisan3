"use client";

import type { components } from "@/api/openapi";
import { EmptyState, EntityLink, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { useApiResource } from "@/lib/use-api-resource";
import { useState } from "react";

type AuditLog = components["schemas"]["AuditLogResponse"];

export default function AuditPage() {
  const [entityType, setEntityType] = useState("");
  const [entityId, setEntityId] = useState("");
  const [query, setQuery] = useState("/api/audit?limit=100");
  const audit = useApiResource<AuditLog[]>(query);

  function applyFilters(event: React.FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams({ limit: "100" });
    if (entityType.trim()) params.set("entity_type", entityType.trim());
    if (entityId.trim()) params.set("entity_id", entityId.trim());
    setQuery(`/api/audit?${params.toString()}`);
  }

  function clearFilters() {
    setEntityType("");
    setEntityId("");
    setQuery("/api/audit?limit=100");
  }

  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="AUDIT-LOG · Golden Production"
        title="سجل التدقيق"
        description="عرض قراءة فقط للأحداث التي كتبها النظام. المرشحات تغيّر الاستعلام ولا تنشئ سجلات أو تفسيرات جديدة."
        actions={<span className="status-badge status-information"><span aria-hidden="true">●</span> Read-only API</span>}
      />

      <Panel title="مرشحات السجل" eyebrow="Backend-supported filters">
        <form className="form-grid form-grid-3" onSubmit={applyFilters}>
          <label className="form-field">
            <span>نوع الكيان</span>
            <input id="audit-entity-type" name="entity_type" className="input" value={entityType} onChange={(event) => setEntityType(event.target.value)} placeholder="SemanticClaim" />
          </label>
          <label className="form-field">
            <span>معرّف الكيان</span>
            <input id="audit-entity-id" name="entity_id" className="input technical-text" value={entityId} onChange={(event) => setEntityId(event.target.value)} placeholder="clm_…" />
          </label>
          <div className="form-field">
            <span aria-hidden="true">&nbsp;</span>
            <div className="button-row">
              <button className="button button-primary" type="submit">تطبيق</button>
              <button className="button button-quiet" type="button" onClick={clearFilters}>مسح</button>
            </div>
          </div>
        </form>
      </Panel>

      <Panel title="الأحداث المسجلة" eyebrow="AuditLogResponse">
        {audit.loading && <LoadingState label="جارٍ تحميل سجل التدقيق…" />}
        {audit.error && <ErrorState message={audit.error} retry={audit.reload} />}
        {audit.data && audit.data.length === 0 && (
          <EmptyState title="لا توجد أحداث مطابقة" detail="لم تُنشئ الواجهة سجلات تجريبية لملء هذا العرض." />
        )}
        {audit.data && audit.data.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>الوقت</th>
                  <th>الكيان / المرجع</th>
                  <th>الإجراء</th>
                  <th>الفاعل</th>
                  <th>الانتقال المسجل</th>
                </tr>
              </thead>
              <tbody>
                {audit.data.map((log) => (
                  <tr key={log.id}>
                    <td>{new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(new Date(log.created_at))}</td>
                    <td><strong>{log.entity_type}</strong><small><EntityLink type={log.entity_type} id={log.entity_id} /></small></td>
                    <td><span className="status-badge status-information"><span aria-hidden="true">●</span>{log.action}</span></td>
                    <td>{log.actor}</td>
                    <td><span className="technical-text">{log.previous_state ?? "—"}</span> ← <span className="technical-text">{log.new_state ?? "—"}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </main>
  );
}
