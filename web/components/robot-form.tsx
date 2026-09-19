"use client";

import { FormEvent, useState, useTransition } from "react";
import { useRouter } from "next/navigation";

import { createRobot, updateRobot, type RobotDetail } from "@/lib/api";

type Mode = "create" | "edit";

type RobotFormProps = {
  mode: Mode;
  initial?: RobotDetail;
};

const STATUS_OPTIONS = ["active", "idle", "maintenance", "offline"];

function toDateTimeLocal(value: string | null | undefined): string {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  const pad = (part: number) => String(part).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function optionalText(value: FormDataEntryValue | null): string | null {
  const text = String(value ?? "").trim();
  return text.length ? text : null;
}

export function RobotForm({ mode, initial }: RobotFormProps) {
  const router = useRouter();
  const [error, setError] = useState<string>("");
  const [isPending, startTransition] = useTransition();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    const formData = new FormData(event.currentTarget);
    const payload: Record<string, unknown> = {
      robot_name: optionalText(formData.get("robot_name")),
      vendor: optionalText(formData.get("vendor")),
      model: optionalText(formData.get("model")),
      serial_number: optionalText(formData.get("serial_number")),
      controller_type: optionalText(formData.get("controller_type")),
      firmware_version: optionalText(formData.get("firmware_version")),
      site: optionalText(formData.get("site")),
      line: optionalText(formData.get("line")),
      cell_name: optionalText(formData.get("cell_name")),
      status: String(formData.get("status") ?? "active"),
      description: optionalText(formData.get("description")),
    };

    if (mode === "create") {
      const externalId = String(formData.get("external_id") ?? "").trim();
      if (!externalId) {
        setError("Robot ID is required.");
        return;
      }
      payload.external_id = externalId;
    }

    const installedAt = String(formData.get("installed_at") ?? "").trim();
    if (installedAt) {
      payload.installed_at = new Date(installedAt).toISOString();
    } else if (mode === "edit") {
      payload.installed_at = null;
    }

    const metadataText = String(formData.get("metadata_json") ?? "").trim();
    if (metadataText) {
      try {
        payload.metadata_json = JSON.parse(metadataText);
      } catch {
        setError("Extended metadata must be valid JSON.");
        return;
      }
    } else if (mode === "edit") {
      payload.metadata_json = null;
    }

    startTransition(async () => {
      try {
        const saved =
          mode === "create"
            ? await createRobot(payload)
            : await updateRobot(initial!.robot_id, payload);
        router.push(`/robots/${saved.robot_id}`);
        router.refresh();
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Failed to save robot.");
      }
    });
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <div className="form-row">
        <label>
          Robot ID {mode === "edit" ? "(read-only)" : ""}
          <input
            defaultValue={initial?.robot_id ?? ""}
            disabled={mode === "edit"}
            name="external_id"
            placeholder="robot-01"
            required={mode === "create"}
          />
        </label>
        <label>
          Name
          <input defaultValue={initial?.robot_name ?? ""} name="robot_name" placeholder="Welding Robot 01" />
        </label>
      </div>

      <div className="form-row">
        <label>
          Vendor
          <input defaultValue={initial?.vendor ?? ""} name="vendor" placeholder="KUKA" />
        </label>
        <label>
          Model
          <input defaultValue={initial?.model ?? ""} name="model" placeholder="KR 10 R1100" />
        </label>
      </div>

      <div className="form-row">
        <label>
          Serial Number
          <input defaultValue={initial?.serial_number ?? ""} name="serial_number" />
        </label>
        <label>
          Controller
          <input defaultValue={initial?.controller_type ?? ""} name="controller_type" placeholder="KR C5" />
        </label>
      </div>

      <div className="form-row">
        <label>
          Firmware
          <input defaultValue={initial?.firmware_version ?? ""} name="firmware_version" placeholder="8.6" />
        </label>
        <label>
          Status
          <select defaultValue={initial?.status ?? "active"} name="status">
            {STATUS_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="form-row">
        <label>
          Site
          <input defaultValue={initial?.site ?? ""} name="site" placeholder="Plant A" />
        </label>
        <label>
          Line
          <input defaultValue={initial?.line ?? ""} name="line" placeholder="Line 1" />
        </label>
      </div>

      <div className="form-row">
        <label>
          Cell
          <input defaultValue={initial?.cell_name ?? ""} name="cell_name" placeholder="Cell A" />
        </label>
        <label>
          Installed At
          <input defaultValue={toDateTimeLocal(initial?.installed_at)} name="installed_at" type="datetime-local" />
        </label>
      </div>

      <label>
        Description
        <textarea defaultValue={initial?.description ?? ""} name="description" rows={3} />
      </label>

      <label>
        Extended Metadata (JSON)
        <textarea
          defaultValue={initial?.metadata_json ? JSON.stringify(initial.metadata_json, null, 2) : ""}
          name="metadata_json"
          placeholder='{"payload_kg": 10, "reach_mm": 1100}'
          rows={4}
        />
      </label>

      {error ? <p className="form-error">{error}</p> : null}

      <div className="form-actions">
        <button className="button" disabled={isPending} type="submit">
          {isPending ? "Saving..." : mode === "create" ? "Register Robot" : "Save Changes"}
        </button>
        <button className="button-secondary" onClick={() => router.back()} type="button">
          Cancel
        </button>
      </div>
    </form>
  );
}
