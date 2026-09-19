import Link from "next/link";
import { notFound } from "next/navigation";

import { getRecommendations, getRobot, getRobotTelemetry } from "@/lib/api";
import { formatDate } from "@/lib/format";

type PageProps = {
  params: Promise<{ robotId: string }>;
};

export default async function RobotDetailPage({ params }: PageProps) {
  const { robotId } = await params;

  const robot = await getRobot(robotId).catch(() => null);
  if (!robot) {
    notFound();
  }

  const [telemetry, recommendations] = await Promise.all([
    getRobotTelemetry(robotId, 10),
    getRecommendations(robotId),
  ]);

  const metadataEntries = Object.entries(robot.metadata_json ?? {});

  return (
    <>
      <section className="panel">
        <div className="card-header">
          <div>
            <p className="eyebrow">Robot Detail</p>
            <h2>{robot.robot_name || robot.robot_id}</h2>
            <p className="muted">{robot.description || "No description"}</p>
          </div>
          <div className="detail-actions">
            <span className={`badge status ${robot.status}`}>{robot.status}</span>
            <Link className="button-secondary" href={`/robots/${robot.robot_id}/edit`}>
              Edit
            </Link>
            <Link className="button-secondary" href="/robots">
              Back to fleet
            </Link>
          </div>
        </div>

        <div className="details-grid">
          <div className="detail-pill">
            <strong>Robot ID</strong>
            {robot.robot_id}
          </div>
          <div className="detail-pill">
            <strong>Vendor</strong>
            {robot.vendor || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Model</strong>
            {robot.model || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Serial Number</strong>
            {robot.serial_number || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Controller</strong>
            {robot.controller_type || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Firmware</strong>
            {robot.firmware_version || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Site</strong>
            {robot.site || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Line</strong>
            {robot.line || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Cell</strong>
            {robot.cell_name || "n/a"}
          </div>
          <div className="detail-pill">
            <strong>Installed</strong>
            {formatDate(robot.installed_at)}
          </div>
          <div className="detail-pill">
            <strong>Registered</strong>
            {formatDate(robot.created_at)}
          </div>
          <div className="detail-pill">
            <strong>Updated</strong>
            {formatDate(robot.updated_at)}
          </div>
        </div>

        {metadataEntries.length ? (
          <div className="meta-block">
            <p className="eyebrow">Extended Metadata</p>
            <div className="details-grid">
              {metadataEntries.map(([key, value]) => (
                <div className="detail-pill" key={key}>
                  <strong>{key}</strong>
                  {String(value)}
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </section>

      <section className="two-column section-gap">
        <article className="panel">
          <div className="card-header">
            <div>
              <h3>Recent Telemetry</h3>
              <p className="muted">Latest {telemetry.length} samples.</p>
            </div>
          </div>
          {telemetry.length ? (
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>Observed</th>
                    <th>Source</th>
                    <th>Payload</th>
                  </tr>
                </thead>
                <tbody>
                  {telemetry.map((record) => (
                    <tr key={record.id}>
                      <td>{formatDate(record.observed_at)}</td>
                      <td>{record.source}</td>
                      <td>{Object.entries(record.payload).map(([key, value]) => `${key}=${value}`).join(", ")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="empty">No telemetry recorded yet.</div>
          )}
        </article>

        <article className="panel">
          <div className="card-header">
            <div>
              <h3>Recommendations</h3>
              <p className="muted">{recommendations.length} open items.</p>
            </div>
          </div>
          {recommendations.length ? (
            <div className="list">
              {recommendations.map((recommendation) => (
                <div className="list-item" key={recommendation.id}>
                  <div className="row">
                    <div>
                      <h4>{recommendation.recommendation_type}</h4>
                      <p>{recommendation.message}</p>
                    </div>
                    <span className={`badge ${recommendation.risk_level}`}>{recommendation.risk_level}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty">No recommendations for this robot.</div>
          )}
        </article>
      </section>
    </>
  );
}
