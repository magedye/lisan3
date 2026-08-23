"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AskLisan() {
  const [expression, setExpression] = useState("");
  const [contractType, setContractType] = useState("ROOT_CORE");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [claim, setClaim] = useState<any>(null);
  const router = useRouter();

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression, contract_type: contractType })
      });
      const data = await res.json();
      setResult(data.status);
      setClaim(data.claim);
    } catch (err) {
      console.error(err);
      setResult("ERROR");
    } finally {
      setLoading(false);
    }
  };

  const startResearch = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_contract: contractType,
          target_expression: expression,
          methodology_revision: "v7.1",
          corpus_snapshot: "current",
          authority_context: { initiator: "local_user" }
        })
      });
      const runData = await res.json();
      router.push(`/run/${runData.id}`);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-12 bg-slate-50 flex justify-center items-start">
      <div className="w-full max-w-2xl bg-white p-8 rounded-xl shadow-sm border border-slate-200 mt-20">
        <h1 className="text-3xl font-bold text-slate-800 mb-6">اسأل لسان (Ask Lisan)</h1>
        
        <form onSubmit={handleAsk} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Target Expression</label>
            <input 
              type="text" 
              value={expression}
              onChange={(e) => setExpression(e.target.value)}
              className="w-full border border-slate-300 rounded-md p-2"
              placeholder="e.g. ضرب"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Contract Type</label>
            <select 
              value={contractType}
              onChange={(e) => setContractType(e.target.value)}
              className="w-full border border-slate-300 rounded-md p-2"
            >
              <option value="ROOT_CORE">Root Core (المعنى المحوري)</option>
              <option value="LOCAL_MEANING">Local Meaning (المعنى الموضعي)</option>
            </select>
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-2 rounded-md transition-colors"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {result === "INSUFFICIENT_EVIDENCE" && (
          <div className="mt-8 p-6 bg-amber-50 border border-amber-200 rounded-md">
            <h3 className="text-lg font-semibold text-amber-800">Insufficient Evidence</h3>
            <p className="text-amber-700 mt-1">
              No locked semantic claim exists for <strong>{expression}</strong> ({contractType}).
            </p>
            <button 
              onClick={startResearch}
              className="mt-4 px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-md text-sm font-medium transition-colors"
            >
              Start Research Run
            </button>
          </div>
        )}

        {result === "FOUND" && claim && (
          <div className="mt-8 p-6 bg-green-50 border border-green-200 rounded-md">
            <h3 className="text-lg font-semibold text-green-800">Found Locked Claim</h3>
            <p className="text-green-700 mt-1">Status: {claim.official_status}</p>
          </div>
        )}
      </div>
    </main>
  );
}
