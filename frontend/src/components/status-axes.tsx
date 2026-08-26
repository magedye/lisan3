type StatusAxesProps = {
  epistemic: string;
  review: string;
  freshness: string;
  publication: string;
  compact?: boolean;
};

const labels = {
  epistemic: "الحالة المعرفية",
  review: "المراجعة",
  freshness: "الحداثة",
  publication: "النشر",
};

type StatusAxis = keyof typeof labels;

const axisValues: Record<StatusAxis, ReadonlySet<string>> = {
  epistemic: new Set(["OBSERVATION", "HYPOTHESIS", "TESTED", "SUPPORTED", "LOCK_BLOCKED", "LOCK_INTERNAL_RESULT", "REJECTED", "UNRESOLVED"]),
  review: new Set(["NOT_REVIEWED", "REVIEW_REQUIRED", "IN_REVIEW", "APPROVED", "REJECTED", "OWNER_DECISION_REQUIRED"]),
  freshness: new Set(["CURRENT", "STALE", "INVALIDATED", "REVALIDATION_REQUIRED"]),
  publication: new Set(["PRIVATE_WORKING", "REVIEWABLE", "PUBLISHABLE", "PUBLISHED", "WITHDRAWN"]),
};

function toneForValue(value: string) {
  if (["REJECTED", "FAILED", "FAIL", "CONTAMINATED", "INVALIDATED"].includes(value)) return "danger";
  if (["STALE", "REVALIDATION_REQUIRED"].includes(value)) return "stale";
  if (["REVIEW_REQUIRED", "IN_REVIEW", "OWNER_DECISION_REQUIRED", "LOCK_BLOCKED"].includes(value)) return "warning";
  if (["SUPPORTED", "APPROVED", "CURRENT", "PUBLISHED", "PASSED", "PASS", "CLEAN", "AVAILABLE"].includes(value)) return "positive";
  if (["OBSERVATION", "HYPOTHESIS", "TESTED", "LOCK_INTERNAL_RESULT", "REVIEWABLE", "PUBLISHABLE", "ACTIVE"].includes(value)) return "information";
  return "neutral";
}

function axisTone(axis: StatusAxis, value: string) {
  if (!axisValues[axis].has(value)) return "neutral";
  if (axis === "publication" && ["PRIVATE_WORKING", "WITHDRAWN"].includes(value)) return "neutral";
  if (axis === "review" && value === "NOT_REVIEWED") return "neutral";
  if (axis === "epistemic" && value === "UNRESOLVED") return "neutral";
  return toneForValue(value);
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

export function StatusAxes({ epistemic, review, freshness, publication, compact }: StatusAxesProps) {
  return (
    <dl className={`status-axes${compact ? " status-axes-compact" : ""}`} aria-label="محاور الحالة الأربعة المستقلة">
      {Object.entries({ epistemic, review, freshness, publication }).map(([axis, value]) => {
        const statusAxis = axis as StatusAxis;
        const canonical = axisValues[statusAxis].has(value);
        return (
          <div key={axis} className={`status-axis status-${axisTone(statusAxis, value)}`} data-contract-defect={canonical ? undefined : "true"}>
            <dt>{labels[statusAxis]}</dt>
            <dd dir="ltr">{value}{!canonical && <small className="technical-text"> CONTRACT_DEFECT</small>}</dd>
          </div>
        );
      })}
    </dl>
  );
}
