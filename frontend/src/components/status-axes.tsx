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

function toneFor(value: string) {
  if (/REJECTED|FAIL|CONTAMINATED|INVALIDATED/.test(value)) return "danger";
  if (/STALE|REVALIDATION/.test(value)) return "stale";
  if (/REVIEW|PENDING|OWNER|BLOCKED/.test(value)) return "warning";
  if (/SUPPORTED|APPROVED|CURRENT|PUBLISHED|PASS|CLEAN/.test(value)) return "positive";
  if (/HYPOTHESIS|INTERNAL|REVIEWABLE|ACTIVE/.test(value)) return "information";
  return "neutral";
}

export function StatusBadge({ label, value }: { label: string; value: string }) {
  return (
    <span className={`status-badge status-${toneFor(value)}`} aria-label={`${label}: ${value}`}>
      <span aria-hidden="true">●</span>
      <span>{label}</span>
      <b dir="ltr">{value}</b>
    </span>
  );
}

export function StatusAxes({ epistemic, review, freshness, publication, compact }: StatusAxesProps) {
  return (
    <dl className={`status-axes${compact ? " status-axes-compact" : ""}`} aria-label="محاور الحالة الأربعة المستقلة">
      {Object.entries({ epistemic, review, freshness, publication }).map(([axis, value]) => (
        <div key={axis} className={`status-axis status-${toneFor(value)}`}>
          <dt>{labels[axis as keyof typeof labels]}</dt>
          <dd dir="ltr">{value}</dd>
        </div>
      ))}
    </dl>
  );
}
