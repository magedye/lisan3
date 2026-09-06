type ResearchStatusProps = {
  research: string;
  canonical: string;
  strength?: string;
  verification?: string;
  compact?: boolean;
};

const researchValues = new Set(["PREFERRED", "UNRESOLVED", "REJECTED"]);
const canonicalValues = new Set(["NOT_CANONICAL", "ACCEPTED", "REOPEN_REQUIRED"]);

function toneForValue(value: string) {
  if (["REJECTED", "FAILED", "CONTAMINATED"].includes(value)) return "danger";
  if (["REOPEN_REQUIRED", "NOT_VERIFIED"].includes(value)) return "stale";
  if (["UNRESOLVED", "NOT_CANONICAL", "WEAK", "MODERATE"].includes(value)) return "warning";
  if (["PREFERRED", "ACCEPTED", "STRONG", "VERIFIED", "PASSED", "CLEAN", "AVAILABLE"].includes(value)) return "positive";
  return "neutral";
}

export function StatusBadge({ label, value }: { label: string; value: string }) {
  return (
    <span className={`status-badge status-${toneForValue(value)}`} aria-label={`${label}: ${value}`}>
      <span aria-hidden="true">●</span>
      <span>{label}</span>
      <b dir="ltr">{value}</b>
    </span>
  );
}

export function ResearchStatus({ research, canonical, strength, verification, compact }: ResearchStatusProps) {
  const facts = [
    { key: "research", label: "حالة البحث", value: research, valid: researchValues.has(research) },
    { key: "canonical", label: "الحالة المعتمدة", value: canonical, valid: canonicalValues.has(canonical) },
    ...(compact ? [] : [
      { key: "strength", label: "قوة النتيجة", value: strength ?? "UNAVAILABLE", valid: Boolean(strength) },
      { key: "verification", label: "التحقق", value: verification ?? "UNAVAILABLE", valid: Boolean(verification) },
    ]),
  ];
  return (
    <dl className={`status-axes${compact ? " status-axes-compact" : ""}`} aria-label="حالة البحث والاعتماد">
      {facts.map((fact) => (
        <div key={fact.key} className={`status-axis status-${toneForValue(fact.value)}`} data-contract-defect={fact.valid ? undefined : "true"}>
          <dt>{fact.label}</dt>
          <dd dir="ltr">{fact.value}{!fact.valid && <small className="technical-text"> CONTRACT_DEFECT</small>}</dd>
        </div>
      ))}
    </dl>
  );
}
