"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { href: "/", label: "مركز الانتباه", marker: "⌂" },
  { href: "/governance", label: "الحوكمة", marker: "◇" },
  { href: "/steward", label: "مركز المشرف", marker: "△" },
  { href: "/audit", label: "سجل التدقيق", marker: "≡" },
];

function isActive(pathname: string, href: string) {
  return href === "/" ? pathname === href : pathname.startsWith(href);
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <Link className="brand" href="/" aria-label="لسان — الصفحة الرئيسية">
          <span className="brand-mark" aria-hidden="true">ل</span>
          <span>
            <strong>لسان</strong>
            <small>منصة البحث الدلالي المحكوم</small>
          </span>
        </Link>

        <nav className="primary-nav" aria-label="التنقل الرئيسي">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={isActive(pathname, item.href) ? "active" : undefined}
              aria-current={isActive(pathname, item.href) ? "page" : undefined}
            >
              <span aria-hidden="true">{item.marker}</span>
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="sidebar-context">
          <span className="status-dot" aria-hidden="true" />
          <span>
            <strong>مساحة عمل محلية</strong>
            <small>البيانات المعروضة من العقود الفعلية فقط</small>
          </span>
        </div>
      </aside>

      <div className="app-content">
        <header className="topbar">
          <span>بيئة لسان البحثية</span>
          <span className="context-chip">RTL · Trusted local</span>
        </header>
        {children}
      </div>
    </div>
  );
}
