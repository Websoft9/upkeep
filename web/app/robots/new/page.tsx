import Link from "next/link";

import { RobotForm } from "@/components/robot-form";

export default function NewRobotPage() {
  return (
    <section className="panel">
      <div className="card-header">
        <div>
          <p className="eyebrow">Robots</p>
          <h2>Register Robot</h2>
          <p className="muted">Create the asset record and metadata for a robot before telemetry arrives.</p>
        </div>
        <Link className="button-secondary" href="/robots">
          Back to fleet
        </Link>
      </div>

      <RobotForm mode="create" />
    </section>
  );
}
