import Link from "next/link";
import { notFound } from "next/navigation";

import { RobotForm } from "@/components/robot-form";
import { getRobot } from "@/lib/api";

type PageProps = {
  params: Promise<{ robotId: string }>;
};

export default async function EditRobotPage({ params }: PageProps) {
  const { robotId } = await params;

  const robot = await getRobot(robotId).catch(() => null);
  if (!robot) {
    notFound();
  }

  return (
    <section className="panel">
      <div className="card-header">
        <div>
          <p className="eyebrow">Robots</p>
          <h2>Edit {robot.robot_name || robot.robot_id}</h2>
          <p className="muted">Update asset metadata, location, and operating status.</p>
        </div>
        <Link className="button-secondary" href={`/robots/${robot.robot_id}`}>
          Back to detail
        </Link>
      </div>

      <RobotForm initial={robot} mode="edit" />
    </section>
  );
}
