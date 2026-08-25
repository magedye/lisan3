"use client";

import type { components } from "@/api/openapi";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type QualityProfile = components["schemas"]["QualityProfileResponse"];
type ReproductionManifest = components["schemas"]["ReproductionManifestResponse"];
type Provenance = {
  corpus_snapshot: string;
  dependencies: unknown[];
  audit_trail: unknown[];
};

export default function ClaimPage() {
  const params = useParams();
  const claimId = params.id as string;

  const [provenance, setProvenance] = useState<Provenance | null>(null);
  const [quality, setQuality] = useState<QualityProfile | null>(null);
  const [manifest, setManifest] = useState<ReproductionManifest | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchClaimData() {
      try {
        const provRes = await fetch(`/api/claims/${claimId}/provenance`);
        if (provRes.ok) setProvenance((await provRes.json()) as Provenance);

        const qualRes = await fetch(`/api/claims/${claimId}/quality`);
        if (qualRes.ok) setQuality((await qualRes.json()) as QualityProfile);

        const manRes = await fetch(`/api/claims/${claimId}/reproduction_manifest`);
        if (manRes.ok) setManifest((await manRes.json()) as ReproductionManifest);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchClaimData();
  }, [claimId]);

  if (loading) return <div>Loading claim data...</div>;

  return (
    <div className="p-8">
      <h1>Claim: {claimId}</h1>

      <section>
        <h2>Provenance</h2>
        {provenance ? (
          <div>
            <span id="prov-corpus">{provenance.corpus_snapshot}</span>
            <span id="prov-deps">{provenance.dependencies?.length || 0} dependencies</span>
            <span id="prov-audit">{provenance.audit_trail?.length || 0} audit logs</span>
          </div>
        ) : (
          <p>No provenance data</p>
        )}
      </section>

      <section>
        <h2>Quality & Purity</h2>
        {quality ? (
          <div>
            <span id="qual-score">Score: {quality.purity_score}</span>
            <span id="qual-rating">Rating: {quality.purity_rating}</span>
            <span id="qual-findings">{quality.purity_findings?.length || 0} findings</span>
          </div>
        ) : (
          <p>No quality data</p>
        )}
      </section>

      <section>
        <h2>Reproduction Manifest</h2>
        {manifest ? (
          <div>
            <span id="man-corpus">{manifest.corpus_snapshot_id}</span>
            <span id="man-deps">{manifest.dependencies?.length || 0} dependencies</span>
          </div>
        ) : (
          <p>No manifest data</p>
        )}
      </section>
    </div>
  );
}
