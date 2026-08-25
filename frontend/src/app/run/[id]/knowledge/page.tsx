"use client";

import type { components } from "@/api/openapi";
import { EmptyState, ErrorState, LoadingState, PageHeader, Panel } from "@/components/page-primitives";
import { StatusBadge } from "@/components/status-axes";
import { useApiResource } from "@/lib/use-api-resource";
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";
import { useParams } from "next/navigation";
import { useMemo } from "react";

type KnowledgeGraph = components["schemas"]["KnowledgeGraphResponse"];

function edgeColor(origin: string) {
  if (origin === "DISCOVERY_CANDIDATE") return "#d97706";
  if (origin === "GOVERNED_ASSERTION") return "#0f766e";
  return "#475569";
}

export default function KnowledgeExplorerPage() {
  const params = useParams();
  const runId = params.id as string;
  const graph = useApiResource<KnowledgeGraph>(`/api/runs/${runId}/knowledge-graph`);

  const flowNodes = useMemo<Node[]>(() => graph.data?.nodes.map((node, index) => ({
    id: node.node_id,
    position: { x: (index % 3) * 260, y: Math.floor(index / 3) * 155 },
    data: { label: `${node.entity_type}: ${node.entity_id}` },
    style: { border: "1px solid #64748b", borderRadius: 6, background: "#fff", color: "#0f172a", fontSize: 12, padding: 10, width: 210 },
  })) ?? [], [graph.data]);

  const flowEdges = useMemo<Edge[]>(() => graph.data?.edges.map((edge) => ({
    id: edge.edge_id,
    source: edge.source_node_id,
    target: edge.target_node_id,
    label: edge.edge_type,
    style: { stroke: edgeColor(edge.edge_origin), strokeWidth: 2 },
    labelStyle: { fill: "#334155", fontSize: 11 },
  })) ?? [], [graph.data]);

  if (graph.loading) return <main className="page-frame"><LoadingState label="جارٍ تحميل إسقاط المعرفة R1…" /></main>;
  if (graph.error) return (
    <main className="page-frame" data-testid="knowledge-graph-blocked">
      <PageHeader eyebrow="R1 · Read-only projection" title="مستكشف المعرفة" description="الإسقاط يفشل مغلقاً عندما لا تسمح حدود القفل والعزل بالقراءة." />
      <ErrorState message={graph.error} retry={graph.reload} />
    </main>
  );
  if (!graph.data) return <main className="page-frame"><EmptyState title="لا يوجد إسقاط" detail="لم يرجع backend بيانات Graph لهذا التشغيل." /></main>;

  const data = graph.data;
  return (
    <main className="page-frame">
      <PageHeader
        eyebrow="R1_INDEPENDENTLY_CONFIRMED · Derived Projection"
        title="مستكشف المعرفة"
        description="الرسم يوضح الاتصال البنيوي والمصدر. لا يثبت حقيقة دلالية ولا يحوّل المرشح إلى معرفة محكومة."
        actions={<StatusBadge label="السلطة" value="DERIVED_READ_ONLY" />}
      />

      <div className="context-strip" data-testid="graph-authority-notice">
        <span>{data.authority_notice}</span>
        <span>Projection <b className="technical-text">{data.projection_revision}</b></span>
        <span>Run <b className="technical-text">{runId}</b></span>
      </div>

      <section className="metric-grid" aria-label="جرد الإسقاط">
        <article className="metric-card information"><span>العقد</span><strong>{data.analysis.node_count}</strong><small>Derived nodes</small></article>
        <article className="metric-card positive"><span>الروابط</span><strong>{data.analysis.edge_count}</strong><small>Typed edges</small></article>
        <article className="metric-card warning"><span>عقد الدورات</span><strong>{data.analysis.cycle_node_ids.length}</strong><small>تحليل بنيوي فقط</small></article>
        <article className="metric-card stale"><span>العقد القابلة للوصول</span><strong>{data.analysis.reachable_node_ids.length}</strong><small>ليست درجة ثقة</small></article>
      </section>

      <Panel title="الإسقاط التفاعلي" eyebrow="React Flow · no writes">
        {data.nodes.length === 0 ? <EmptyState title="الإسقاط فارغ" detail="لا توجد عقد أو روابط مشتقة متاحة لهذا التشغيل." /> : (
          <div className="graph-canvas" data-testid="knowledge-graph-flow" role="img" aria-label={`رسم معرفي مشتق يحوي ${data.nodes.length} عقدة و${data.edges.length} رابطاً`}>
            <ReactFlow nodes={flowNodes} edges={flowEdges} fitView nodesDraggable={false} nodesConnectable={false} elementsSelectable={false} panOnDrag zoomOnScroll proOptions={{ hideAttribution: true }}>
              <Background />
              <Controls showInteractive={false} />
              <MiniMap pannable zoomable />
            </ReactFlow>
          </div>
        )}
      </Panel>

      <Panel title="البديل النصي الكامل" eyebrow="Provenance and authority table">
        {data.edges.length === 0 ? <EmptyState title="لا توجد روابط" detail="الرسم والجدول يعكسان الحالة الفعلية نفسها." /> : (
          <div className="table-wrap" data-testid="graph-provenance-table">
            <table>
              <thead><tr><th>العلاقة</th><th>الأصل</th><th>الحالة</th><th>مرجع المصدر</th></tr></thead>
              <tbody>{data.edges.map((edge) => (
                <tr key={edge.edge_id}>
                  <td className="technical-text">{edge.edge_type}</td>
                  <td><StatusBadge label="الأصل" value={edge.edge_origin} /><small>{edge.presentation_label}</small></td>
                  <td><StatusBadge label="الحالة" value={edge.edge_status} /></td>
                  <td className="technical-text">{edge.provenance_ref}</td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        )}
      </Panel>
    </main>
  );
}
