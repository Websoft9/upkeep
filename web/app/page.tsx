import { DashboardActions } from "@/components/dashboard-actions";
import { TelemetryForm } from "@/components/telemetry-form";
import { getApiBaseUrl, getHealth, getRecommendations, getRobots } from "@/lib/api";
import { formatDate } from "@/lib/format";

export default async function DashboardPage() {
  const [health, robots, recommendations] = await Promise.all([getHealth(), getRobots(), getRecommendations()]);

  const highRiskCount = recommendations.filter((recommendation) => recommendation.risk_level === "high").length;
  const mediumRiskCount = recommendations.filter((recommendation) => recommendation.risk_level === "medium").length;

  return (
    <>
      <section className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">Walking Skeleton</p>
          <h2>Telemetry in. Maintenance decisions out.</h2>
          <p>
            This dashboard sits on top of the live FastAPI backend. It shows seeded or ingested robot telemetry,
            surfaces predictive maintenance recommendations, and gives developers an immediate way to feel the product.
          </p>
          <p className="muted">API base URL: {getApiBaseUrl()}</p>
        </div>
        <DashboardActions />
      </section>

      <section className="grid metrics">
        <article className="metric-card">
          <p className="metric-label">Backend Health</p>
          <p className="metric-value">{health.status}</p>
          <p className="metric-note">FastAPI connection status</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Tracked Robots</p>
          <p className="metric-value">{robots.length}</p>
          <p className="metric-note">Robot identities known to the system</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">High Risk Recommendations</p>
          <p className="metric-value">{highRiskCount}</p>
          <p className="metric-note">Items needing the fastest maintenance attention</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Medium Risk Recommendations</p>
          <p className="metric-value">{mediumRiskCount}</p>
          <p className="metric-note">Emerging issues to plan around</p>
        </article>
      </section>

      <section className="split">
        <article className="list-card">
          <div className="card-header">
            <div>
              <h3>Latest Recommendations</h3>
              <p className="muted">The most recent maintenance outputs from the backend rule engine.</p>
            </div>
          </div>
          <div className="list">
            {recommendations.length ? (
              recommendations.slice(0, 5).map((recommendation) => (
                <div className="list-item" key={recommendation.id}>
                  <div className="row">
                    <div>
                      <h4>{recommendation.robot_id}</h4>
                      <p>{recommendation.recommendation_type}</p>
                    </div>
                    <span className={`badge ${recommendation.risk_level}`}>{recommendation.risk_level}</span>
                  </div>
                  <p>{recommendation.message}</p>
                  <div className="details-grid">
                    <div className="detail-pill">
                      <strong>Observed</strong>
                      {String(recommendation.evidence.observed ?? "n/a")}
                    </div>
                    <div className="detail-pill">
                      <strong>Threshold</strong>
                      {String(recommendation.evidence.threshold ?? "n/a")}
                    </div>
                    <div className="detail-pill">
                      <strong>Created</strong>
                      {formatDate(recommendation.created_at)}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty">No recommendations yet. Seed demo data or send telemetry from the simulator.</div>
            )}
          </div>
        </article>

        <TelemetryForm />
      </section>
    </>
  );
}
