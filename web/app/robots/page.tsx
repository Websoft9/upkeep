import Link from "next/link";

import { getRobots } from "@/lib/api";
import { formatDate } from "@/lib/format";

export default async function RobotsPage() {
  const robots = await getRobots();

  return (
    <section className="panel">
      <div className="card-header">
        <div>
          <p className="eyebrow">Robots</p>
          <h2>Fleet View</h2>
          <p className="muted">Registered robots with vendor, model, location, and live status.</p>
        </div>
        <div className="detail-actions">
          <span className="count-chip">{robots.length} assets</span>
          <Link className="button" href="/robots/new">
            Register Robot
          </Link>
        </div>
      </div>

      <div className="list">
        {robots.length ? (
          robots.map((robot) => (
            <Link className="list-item asset-row" key={robot.robot_id} href={`/robots/${robot.robot_id}`}>
              <div className="row">
                <div>
                  <h3>{robot.robot_name || robot.robot_id}</h3>
                  <p>
                    {robot.vendor || "Unknown vendor"} · {robot.model || "Unknown model"}
                  </p>
                </div>
                <span className={`badge status ${robot.status}`}>{robot.status}</span>
              </div>
              <div className="details-grid">
                <div className="detail-pill">
                  <strong>Robot ID</strong>
                  {robot.robot_id}
                </div>
                <div className="detail-pill">
                  <strong>Site / Line</strong>
                  {robot.site || "n/a"} / {robot.line || "n/a"}
                </div>
                <div className="detail-pill">
                  <strong>Cell</strong>
                  {robot.cell_name || "n/a"}
                </div>
                <div className="detail-pill">
                  <strong>Telemetry</strong>
                  {robot.telemetry_count}
                </div>
                <div className="detail-pill">
                  <strong>Recommendations</strong>
                  {robot.recommendation_count}
                </div>
                <div className="detail-pill">
                  <strong>Latest Observed</strong>
                  {formatDate(robot.latest_observed_at)}
                </div>
              </div>
            </Link>
          ))
        ) : (
          <div className="empty">No robots yet. Seed demo data from the dashboard to populate the list.</div>
        )}
      </div>
    </section>
  );
}
