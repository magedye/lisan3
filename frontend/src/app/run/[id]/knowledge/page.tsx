"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";
import type { components } from "@/api/openapi";

type KnowledgeGraph = components["schemas"]["KnowledgeGraphResponse"];

function edgeColor(origin: string) {
  if (origin === "DISCOVERY_CANDIDATE") return "#d97706";
  if (origin === "GOVERNED_ASSERTION") return "#0f766e";
  return "#475569";
}

export default function KnowledgeExplorerPage() {
  const params = useParams();
  const runId = params.id as string;
  const [graph, setGraph] = useState<KnowledgeGraph | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGraph() {
      try {
        const response = await fetch(`/api/runs/${runId}/knowledge-graph`);
        const body = await response.json();
        if (!response.ok) {
          throw new Error(body.detail || "تعذر تحميل إسقاط المعرفة");
        }
        setGraph(body);
      } catch (reason) {
        setError(reason instanceof Error ? reason.message : "تعذر تحميل إسقاط المعرفة");
      } finally {
        setLoading(false);
      }
    }
    fetchGraph();
  }, [runId]);

  const flowNodes = useMemo<Node[]>(() => {
    if (!graph) return [];
    return graph.nodes.map((node, index) => ({
      id: node.node_id,
      position: { x: (index % 3) * 260, y: Math.floor(index / 3) * 155 },
      data: {
        label: `${node.entity_type}: ${node.entity_id}`,
      },
      style: {
        border: "1px solid #64748b",
        borderRadius: 10,
        background: "#fff",
        color: "#0f172a",
        fontSize: 12,
        padding: 10,
        width: 210,
      },
    }));
  }, [graph]);

  const flowEdges = useMemo<Edge[]>(() => {
    if (!graph) return [];
    return graph.edges.map((edge) => ({
      id: edge.edge_id,
      source: edge.source_node_id,
      target: edge.target_node_id,
      label: edge.edge_type,
      style: { stroke: edgeColor(edge.edge_origin), strokeWidth: 2 },
      labelStyle: { fill: "#334155", fontSize: 11 },
      animated: false,
    }));
  }, [graph]);

  if (loading) {
    return <main className="p-12 text-center">جارٍ تحميل مستكشف المعرفة…</main>;
  }

  if (error) {
    return (
      <main className="p-12" data-testid="knowledge-graph-blocked">
        <h1 className="text-2xl font-bold">مستكشف المعرفة</h1>
        <p className="mt-4 rounded border border-amber-300 bg-amber-50 p-4 text-amber-900">
          {error}
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 p-6 md:p-12">
      <section className="mx-auto max-w-6xl space-y-6">
        <header className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-primary-600">R1 · عرض مشتق للقراءة فقط</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">مستكشف المعرفة</h1>
          <p className="mt-3 max-w-3xl text-slate-700" data-testid="graph-authority-notice">
            {graph?.authority_notice}
          </p>
          <p className="mt-2 text-sm text-slate-500">
            العقدة/الرابط يوضحان البنية والمصدر، ولا يثبتان حقيقة دلالية أو ثقة معرفية.
          </p>
        </header>

        <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-3 flex flex-wrap gap-4 text-sm text-slate-600">
            <span>العقد: {graph?.analysis.node_count ?? 0}</span>
            <span>الروابط: {graph?.analysis.edge_count ?? 0}</span>
            <span>المسار: {runId}</span>
          </div>
          <div className="h-[460px] overflow-hidden rounded-lg border border-slate-200" data-testid="knowledge-graph-flow">
            <ReactFlow
              nodes={flowNodes}
              edges={flowEdges}
              fitView
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable={false}
              panOnDrag
              zoomOnScroll
              proOptions={{ hideAttribution: true }}
            >
              <Background />
              <Controls showInteractive={false} />
              <MiniMap pannable zoomable />
            </ReactFlow>
          </div>
        </section>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">جدول المصدر والسلطة</h2>
          <p className="mt-1 text-sm text-slate-600">
            بديل نصي كامل للرسم؛ علاقات المرشح تبقى موسومة ولا تُعرض كمعرفة مثبتة.
          </p>
          <div className="mt-4 overflow-x-auto" data-testid="graph-provenance-table">
            <table className="min-w-full text-right text-sm">
              <thead className="border-b bg-slate-50 text-slate-700">
                <tr>
                  <th className="p-3">العلاقة</th>
                  <th className="p-3">الأصل</th>
                  <th className="p-3">الحالة</th>
                  <th className="p-3">مرجع المصدر</th>
                </tr>
              </thead>
              <tbody>
                {graph?.edges.map((edge) => (
                  <tr key={edge.edge_id} className="border-b border-slate-100">
                    <td className="p-3 font-mono text-xs">{edge.edge_type}</td>
                    <td className="p-3">{edge.presentation_label}</td>
                    <td className="p-3">{edge.edge_status}</td>
                    <td className="p-3 font-mono text-xs">{edge.provenance_ref}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </section>
    </main>
  );
}
