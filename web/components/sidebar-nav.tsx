"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

type NavItem = {
  href: string;
  label: string;
  hint: string;
  icon: ReactNode;
};

const navItems: NavItem[] = [
  {
    href: "/",
    label: "Dashboard",
    hint: "Line overview",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" />
      </svg>
    ),
  },
  {
    href: "/robots",
    label: "Robots",
    hint: "Fleet & cells",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
        <rect x="4" y="8" width="16" height="12" rx="2.5" />
        <path d="M12 8V4.5" />
        <circle cx="12" cy="3.5" r="1.2" />
        <path d="M9 13h.01M15 13h.01" />
        <path d="M9 17h6" />
      </svg>
    ),
  },
  {
    href: "/recommendations",
    label: "Recommendations",
    hint: "Maintenance queue",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
        <path d="M8 4h8l1 2h2.5A1.5 1.5 0 0 1 21 7.5v12A1.5 1.5 0 0 1 19.5 21h-15A1.5 1.5 0 0 1 3 19.5v-12A1.5 1.5 0 0 1 4.5 6H7z" />
        <path d="M8.5 13.5l2.5 2.5 4.5-5" />
      </svg>
    ),
  },
];

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav className="sidebar-nav">
      <p className="sidebar-section">Operations</p>
      {navItems.map((item) => {
        const active = pathname === item.href;
        return (
          <Link key={item.href} href={item.href} className={`side-link${active ? " active" : ""}`}>
            <span className="side-link-bar" aria-hidden="true" />
            <span className="side-link-icon" aria-hidden="true">
              {item.icon}
            </span>
            <span className="side-link-text">
              <span className="side-link-label">{item.label}</span>
              <span className="side-link-hint">{item.hint}</span>
            </span>
          </Link>
        );
      })}
    </nav>
  );
}
