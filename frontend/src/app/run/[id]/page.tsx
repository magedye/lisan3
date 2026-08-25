"use client";

import type { components } from "@/api/openapi";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type ResearchRun = components["schemas"]["ResearchRunResponse"];

export default function ResearchRunPage() {
  const params = useParams();
  const runId = params.id as string;
  const [run, setRun] = useState<ResearchRun | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRun() {
      try {
        const res = await fetch(`/api/runs/${runId}`);
        if (res.ok) {
          const data = await res.json();
          setRun(data as ResearchRun);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchRun();
  }, [runId]);

  if (loading) return <div className="p-12 text-center">Loading run state...</div>;
  if (!run) return <div className="p-12 text-center text-red-600">Run not found.</div>;

  return (
    <main className="min-h-screen p-12 bg-slate-50">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-center mb-8 border-b pb-4">
          <h1 className="text-2xl font-bold text-slate-800">Research Run</h1>
          <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-mono">{run.id}</span>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase">Target Expression</h3>
            <p className="text-lg font-medium mt-1">{run.target_expression}</p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase">Contract</h3>
            <p className="text-lg font-medium mt-1">{run.target_contract}</p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase">Current Stage</h3>
            <span className="inline-block mt-1 px-2 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded text-sm font-medium">
              {run.current_stage}
            </span>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase">Status</h3>
            <span className="inline-block mt-1 px-2 py-1 bg-green-50 text-green-700 border border-green-200 rounded text-sm font-medium">
              {run.status}
            </span>
          </div>
        </div>

        <div className="bg-slate-50 p-6 rounded-lg border border-slate-200">
          <h2 className="text-lg font-semibold mb-4">Durable Checkpoint Retrieved</h2>
          <p className="text-slate-600 text-sm mb-4">
            The run is initialized and persisted in the local SQLite database. The research process can be resumed from this checkpoint at any time.
          </p>
          <pre className="bg-slate-800 text-green-400 p-4 rounded text-xs overflow-auto" dir="ltr">
            {JSON.stringify(run, null, 2)}
          </pre>
        </div>
      </div>
    </main>
  );
}
