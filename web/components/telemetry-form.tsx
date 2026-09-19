"use client";

import { FormEvent, useState, useTransition } from "react";
import { useRouter } from "next/navigation";

import { ingestTelemetry } from "@/lib/api";

const initialValues = {
  source: "nextjs-ui",
  robot_id: "robot-ui-01",
  robot_name: "UI Demo Robot",
  cell_name: "Cell UI",
  vendor: "DemoVendor",
  temperature_c: "84",
  vibration_mm_s: "9",
  cycle_time_s: "78",
  axis_load_pct: "71",
};

export function TelemetryForm() {
  const [result, setResult] = useState<string>("Ready.");
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const payload = {
      source: formData.get("source"),
      robot_id: formData.get("robot_id"),
      robot_name: formData.get("robot_name") || null,
      cell_name: formData.get("cell_name") || null,
      vendor: formData.get("vendor") || null,
      ts: new Date().toISOString(),
      payload: {
        temperature_c: Number(formData.get("temperature_c")),
        vibration_mm_s: Number(formData.get("vibration_mm_s")),
        cycle_time_s: Number(formData.get("cycle_time_s")),
        axis_load_pct: Number(formData.get("axis_load_pct")),
      },
    };

    startTransition(async () => {
      try {
        const response = await ingestTelemetry(payload);
        setResult(JSON.stringify(response, null, 2));
        router.refresh();
      } catch (error) {
        setResult(error instanceof Error ? error.message : "Failed to ingest telemetry.");
      }
    });
  }

  return (
    <div className="form-card">
      <div className="card-header">
        <div>
          <h3>Telemetry Simulator</h3>
          <p className="muted">Send a synthetic robot payload into the FastAPI backend.</p>
        </div>
      </div>
      <form className="form-grid" onSubmit={handleSubmit}>
        {Object.entries(initialValues).map(([key, value]) => (
          <label key={key}>
            {key}
            <input defaultValue={value} name={key} type={key.includes("_c") || key.includes("_s") || key.includes("pct") ? "number" : "text"} />
          </label>
        ))}
        <button className="button" disabled={isPending} type="submit">
          {isPending ? "Sending..." : "Send Telemetry"}
        </button>
      </form>
      <pre className="code">{result}</pre>
    </div>
  );
}
