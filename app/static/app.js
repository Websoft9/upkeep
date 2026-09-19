async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json();
}

function formatDate(value) {
  if (!value) {
    return "n/a";
  }
  return new Date(value).toLocaleString();
}

function robotItem(robot) {
  return `
    <div class="item">
      <strong>${robot.robot_name || robot.robot_id}</strong>
      <p>ID: ${robot.robot_id}</p>
      <p>Cell: ${robot.cell_name || "n/a"}</p>
      <p>Vendor: ${robot.vendor || "n/a"}</p>
      <p>Telemetry: ${robot.telemetry_count} | Recommendations: ${robot.recommendation_count}</p>
      <p>Latest observed: ${formatDate(robot.latest_observed_at)}</p>
    </div>
  `;
}

function recommendationItem(recommendation) {
  return `
    <div class="item">
      <div class="section-head">
        <strong>${recommendation.robot_id}</strong>
        <span class="badge ${recommendation.risk_level}">${recommendation.risk_level}</span>
      </div>
      <p>${recommendation.recommendation_type}</p>
      <p>${recommendation.message}</p>
      <p>Evidence: ${recommendation.evidence.metric}=${recommendation.evidence.observed}, threshold=${recommendation.evidence.threshold}</p>
      <p>Created: ${formatDate(recommendation.created_at)}</p>
    </div>
  `;
}

async function loadHealth() {
  const health = await fetchJson("/health");
  document.getElementById("health-status").textContent = health.status;
}

async function loadRobots() {
  const robots = await fetchJson("/api/v1/robots");
  document.getElementById("robots-list").innerHTML = robots.length
    ? robots.map(robotItem).join("")
    : '<div class="item"><p>No robots yet.</p></div>';
}

async function loadRecommendations() {
  const recommendations = await fetchJson("/api/v1/recommendations");
  document.getElementById("recommendations-list").innerHTML = recommendations.length
    ? recommendations.map(recommendationItem).join("")
    : '<div class="item"><p>No recommendations yet.</p></div>';
}

async function handleSeed() {
  await fetchJson("/api/v1/demo/seed", { method: "POST" });
  await Promise.all([loadRobots(), loadRecommendations()]);
}

async function handleTelemetrySubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
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

  const result = await fetchJson("/api/v1/telemetry/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  document.getElementById("telemetry-result").textContent = JSON.stringify(result, null, 2);
  await Promise.all([loadRobots(), loadRecommendations()]);
}

document.getElementById("seed-demo").addEventListener("click", () => {
  handleSeed().catch((error) => {
    document.getElementById("telemetry-result").textContent = error.message;
  });
});

document.getElementById("refresh-robots").addEventListener("click", () => {
  loadRobots().catch(console.error);
});

document.getElementById("refresh-recommendations").addEventListener("click", () => {
  loadRecommendations().catch(console.error);
});

document.getElementById("telemetry-form").addEventListener("submit", (event) => {
  handleTelemetrySubmit(event).catch((error) => {
    document.getElementById("telemetry-result").textContent = error.message;
  });
});

Promise.all([loadHealth(), loadRobots(), loadRecommendations()]).catch((error) => {
  document.getElementById("telemetry-result").textContent = error.message;
});
