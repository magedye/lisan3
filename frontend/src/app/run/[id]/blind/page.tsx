"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function BlindLabPage() {
  const params = useParams();
  const runId = params.id as string;
  
  const [run, setRun] = useState<any>(null);
  const [isoState, setIsoState] = useState<any>(null);
  const [corpus, setCorpus] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Observation form
  const [form, setForm] = useState("");
  const [syntax, setSyntax] = useState("");
  const [obsError, setObsError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const runRes = await fetch(`http://localhost:8000/runs/${runId}`);
        if (!runRes.ok) throw new Error("Run not found");
        setRun(await runRes.json());

        const isoRes = await fetch(`http://localhost:8000/runs/${runId}/blind`);
        if (isoRes.ok) {
          const isoData = await isoRes.json();
          setIsoState(isoData);
          
          if (isoData.is_contaminated !== "PRIOR_CONTAMINATED") {
            const corpusRes = await fetch(`http://localhost:8000/runs/${runId}/corpus`);
            if (corpusRes.ok) {
              setCorpus(await corpusRes.json());
            }
          }
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [runId]);

  const startPreflight = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/runs/${runId}/blind/preflight`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_contract: run.target_contract,
          corpus_snapshot: run.corpus_snapshot,
          methodology_reference: run.methodology_revision,
          allowed_sources: ["QURAN_CORPUS"]
        })
      });
      if (res.ok) {
        window.location.reload();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const submitObservation = async (e: React.FormEvent) => {
    e.preventDefault();
    setObsError(null);
    try {
      const res = await fetch(`http://localhost:8000/runs/${runId}/observations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          occurrence_ref: corpus[0]?.id || "unknown",
          form,
          syntax
        })
      });
      const data = await res.json();
      if (!res.ok) {
        setObsError(data.detail[0]?.msg || data.detail || "Validation failed");
      } else {
        alert("Observation recorded successfully!");
        setForm("");
        setSyntax("");
      }
    } catch (err: any) {
      setObsError(err.message);
    }
  };

  const triggerContamination = async () => {
    try {
      await fetch(`http://localhost:8000/runs/${runId}/read_semantic_dictionary`);
      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-12 text-center">Loading Blind Lab state...</div>;
  if (error) return <div className="p-12 text-center text-red-600">{error}</div>;

  return (
    <main className="min-h-screen p-12 bg-slate-50">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-slate-800">Blind Lab Isolation</h1>
            <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-mono">{runId}</span>
          </div>
          <div className="flex space-x-4 space-x-reverse">
            <span className="px-3 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded text-sm font-medium">Stage: {run.current_stage}</span>
            {isoState && (
              <span className={`px-3 py-1 border rounded text-sm font-medium ${isoState.is_contaminated === 'CLEAN' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200'}`}>
                Isolation: {isoState.is_contaminated}
              </span>
            )}
          </div>
        </div>

        {/* Preflight Block */}
        {!isoState && (
          <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4">Isolation Preflight Required</h2>
            <p className="text-slate-600 mb-6">Before corpus analysis, the research run must be formally isolated and its sources locked.</p>
            <button onClick={startPreflight} className="bg-primary-600 hover:bg-primary-500 text-white px-6 py-2 rounded-md font-medium transition-colors">
              Start Preflight Isolation
            </button>
          </div>
        )}

        {/* Contamination Alert */}
        {isoState?.is_contaminated === "PRIOR_CONTAMINATED" && (
          <div className="bg-red-50 border border-red-200 p-8 rounded-xl shadow-sm">
            <h2 className="text-xl font-bold text-red-800 mb-2">Isolation Breached</h2>
            <p className="text-red-700 mb-4">{isoState.contamination_reason}</p>
            <p className="text-red-600 text-sm font-mono p-4 bg-red-100 rounded">Progression to internal lock is permanently blocked for this run.</p>
          </div>
        )}

        {/* Active Lab */}
        {isoState && isoState.is_contaminated === "CLEAN" && (
          <div className="grid grid-cols-2 gap-8">
            {/* Corpus Section */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xl font-semibold mb-4 text-slate-800">Admitted Corpus</h2>
              {corpus.length === 0 ? (
                <p className="text-slate-500 italic">No occurrences found in snapshot: {isoState.corpus_snapshot}</p>
              ) : (
                <div className="space-y-4">
                  {corpus.map((c, i) => (
                    <div key={i} className="p-4 bg-slate-50 border border-slate-100 rounded-md">
                      <div className="flex justify-between mb-2">
                        <span className="text-sm font-bold text-slate-700">{c.expression}</span>
                        <span className="text-xs font-mono text-slate-500">{c.verse_ref}</span>
                      </div>
                      <p className="text-slate-800 font-serif text-lg">{c.text}</p>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="mt-8 border-t pt-4">
                <p className="text-xs text-slate-500 mb-2">Simulation Tools:</p>
                <button onClick={triggerContamination} className="text-xs bg-slate-200 hover:bg-red-200 hover:text-red-800 text-slate-600 px-3 py-1 rounded transition-colors">
                  Simulate Prohibited Semantic Read
                </button>
              </div>
            </div>

            {/* Observation Section */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xl font-semibold mb-4 text-slate-800">Record Structural Observation</h2>
              <p className="text-sm text-slate-600 mb-6">Record raw morphological and syntactic observations. Do not include semantic conclusions.</p>
              
              <form onSubmit={submitObservation} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Form (Morphology)</label>
                  <input type="text" value={form} onChange={e => setForm(e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm" placeholder="e.g. past tense verb, pattern fa'ala" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Syntax / Construction</label>
                  <input type="text" value={syntax} onChange={e => setSyntax(e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm" placeholder="e.g. transitive, takes direct object" />
                </div>
                {obsError && <div className="p-3 bg-red-50 text-red-700 border border-red-200 rounded text-sm">{obsError}</div>}
                <button type="submit" className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-2 rounded transition-colors">
                  Save Observation
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
