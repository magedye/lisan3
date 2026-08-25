import Link from "next/link";
import type { ReactNode } from "react";

export function PageHeader({
  eyebrow,
  title,
  description,
  actions,
}: {
  eyebrow: string;
  title: string;
  description: string;
  actions?: ReactNode;
}) {
  return (
    <header className="page-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {actions && <div className="page-actions">{actions}</div>}
    </header>
  );
}

export function Panel({
  title,
  eyebrow,
  action,
  children,
  className = "",
}: {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`panel ${className}`.trim()}>
      <header className="panel-heading">
        <div>
          {eyebrow && <span className="eyebrow">{eyebrow}</span>}
          <h2>{title}</h2>
        </div>
        {action}
      </header>
      {children}
    </section>
  );
}

export function LoadingState({ label = "جارٍ تحميل البيانات…" }: { label?: string }) {
  return (
    <div className="state-card loading-state" role="status" aria-busy="true">
      <span className="loading-mark" aria-hidden="true" />
      <strong>{label}</strong>
    </div>
  );
}

export function EmptyState({ title, detail }: { title: string; detail: string }) {
  return (
    <div className="state-card empty-state">
      <span aria-hidden="true">○</span>
      <strong>{title}</strong>
      <p>{detail}</p>
    </div>
  );
}

export function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return (
    <div className="state-card error-state" role="alert">
      <span aria-hidden="true">!</span>
      <strong>تعذر إكمال الطلب</strong>
      <p>{message}</p>
      {retry && <button className="button button-secondary" onClick={retry}>إعادة المحاولة</button>}
    </div>
  );
}

export function EntityLink({ type, id }: { type: string; id: string }) {
  const href = type === "SemanticClaim" ? `/claims/${id}` : type === "ResearchRun" ? `/run/${id}` : null;
  if (!href) return <span className="technical-text">{id}</span>;
  return <Link className="text-link technical-text" href={href}>{id}</Link>;
}
