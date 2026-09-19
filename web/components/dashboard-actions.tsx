"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";

import { seedDemo } from "@/lib/api";

export function DashboardActions() {
  const [message, setMessage] = useState<string>("");
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  function handleSeed() {
    startTransition(async () => {
      try {
        const result = await seedDemo();
        setMessage(`Seeded ${result.telemetry_created} telemetry records and ${result.recommendations_created} recommendations.`);
        router.refresh();
      } catch (error) {
        setMessage(error instanceof Error ? error.message : "Failed to seed demo data.");
      }
    });
  }

  return (
    <div className="hero-actions">
      <button className="button" onClick={handleSeed} type="button" disabled={isPending}>
        {isPending ? "Seeding..." : "Seed Demo Data"}
      </button>
      <a className="button-secondary" href="/recommendations">
        Open Recommendations
      </a>
      {message ? <p className="muted">{message}</p> : null}
    </div>
  );
}
