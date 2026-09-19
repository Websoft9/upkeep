import { getRecommendations } from "@/lib/api";
import { formatDate } from "@/lib/format";

export default async function RecommendationsPage() {
  const recommendations = await getRecommendations();

  return (
    <section className="panel">
      <div className="card-header">
        <div>
          <p className="eyebrow">Recommendations</p>
          <h2>Maintenance Queue</h2>
          <p className="muted">Explainable maintenance recommendations generated from the current backend rule layer.</p>
        </div>
      </div>

      <div className="list">
        {recommendations.length ? (
          recommendations.map((recommendation) => (
            <article className="list-item" key={recommendation.id}>
              <div className="row">
                <div>
                  <h3>{recommendation.robot_id}</h3>
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
                  <strong>Metric</strong>
                  {String(recommendation.evidence.metric ?? "n/a")}
                </div>
                <div className="detail-pill">
                  <strong>Created</strong>
                  {formatDate(recommendation.created_at)}
                </div>
              </div>
            </article>
          ))
        ) : (
          <div className="empty">No recommendations yet. Use the dashboard to seed data or send telemetry.</div>
        )}
      </div>
    </section>
  );
}
