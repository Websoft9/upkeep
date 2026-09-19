import type { Metadata } from "next";
import { ReactNode } from "react";

import "./globals.css";
import { SidebarNav } from "@/components/sidebar-nav";

export const metadata: Metadata = {
  title: "UpKeep Web",
  description: "Industrial robot maintenance intelligence UI",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <header className="topbar">
            <div className="topbar-brand">
              <span className="logo-mark" aria-hidden="true">
                UK
              </span>
              <div className="brand-copy">
                <span className="brand-name">UpKeep</span>
                <span className="brand-slogan">Robot Maintenance Intelligence</span>
              </div>
            </div>

            <div className="topbar-actions">
              <a className="topbar-link" href="/docs" target="_blank" rel="noreferrer">
                API Docs
              </a>
              <a className="topbar-link" href="/health" target="_blank" rel="noreferrer">
                Health
              </a>
              <div className="user-chip" title="Sign-in coming soon">
                <span className="user-avatar" aria-hidden="true">
                  OP
                </span>
                <span className="user-meta">
                  <span className="user-name">Operator</span>
                  <span className="user-role">Maintenance</span>
                </span>
              </div>
            </div>
          </header>

          <div className="app-body">
            <aside className="sidebar">
              <SidebarNav />
              <div className="sidebar-footer">
                <span className="sidebar-footer-dot" aria-hidden="true" />
                <span>UpKeep v0.1 · dev</span>
              </div>
            </aside>

            <main className="content">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
