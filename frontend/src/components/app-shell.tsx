"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navigation = [
  { href: "/", label: "مركز الانتباه", marker: "⌂", description: "البحث والتشغيلات" },
  { href: "/governance", label: "الحوكمة والمراجعة", marker: "◇", description: "القواعد والقبول" },
  { href: "/steward", label: "Steward", marker: "△", description: "أوامر محكومة" },
  { href: "/audit", label: "التشغيل والتدقيق", marker: "≡", description: "الأحداث والتتبع" },
];

function isActive(pathname: string, href: string) {
  return href === "/" ? pathname === href : pathname.startsWith(href);
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="app-shell">
      <button
        type="button"
        className="mobile-menu-button"
        aria-expanded={menuOpen}
        aria-controls="primary-sidebar"
        onClick={() => setMenuOpen((value) => !value)}
      >
        <span aria-hidden="true">☰</span>
        <span>القائمة</span>
      </button>
      {menuOpen && (
        <button className="sidebar-backdrop" aria-label="إغلاق القائمة" onClick={() => setMenuOpen(false)} />
      )}

      <aside id="primary-sidebar" className={`app-sidebar${menuOpen ? " sidebar-open" : ""}`}>
        <Link className="brand" href="/" aria-label="لـ لسان Lisan Governed Research — الصفحة الرئيسية" onClick={() => setMenuOpen(false)}>
          <span className="brand-mark" aria-hidden="true">لـ</span>
          <span>
            <strong>لسان</strong>
            <small>Lisan Governed Research</small>
          </span>
        </Link>

        <nav className="primary-nav" aria-label="التنقل الرئيسي">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={isActive(pathname, item.href) ? "active" : undefined}
              aria-current={isActive(pathname, item.href) ? "page" : undefined}
              onClick={() => setMenuOpen(false)}
            >
              <span className="nav-marker" aria-hidden="true">{item.marker}</span>
              <span>
                <b>{item.label}</b>
                <small>{item.description}</small>
              </span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-context">
          <span className="status-dot" aria-hidden="true" />
          <span>
            <strong>مساحة عمل محلية موثوقة</strong>
            <small>لا صلاحية معرفية مستنتجة من الواجهة</small>
          </span>
        </div>
      </aside>

      <div className="app-content">
        <header className="topbar">
          <div>
            <strong>بيئة البحث الدلالي المحكوم</strong>
            <span>العقود الفعلية · بيانات محلية</span>
          </div>
          <div className="topbar-actions">
            <Link href="/steward" className="button button-secondary button-small">فتح Steward</Link>
            <span className="context-chip">RTL · LOCAL</span>
          </div>
        </header>
        {children}
      </div>
    </div>
  );
}
