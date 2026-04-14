"use client";

const DASHBOARD_URL = process.env.NEXT_PUBLIC_DASHBOARD_URL || "http://localhost:8501";

export default function DashboardViewer() {
  return (
    <section id="dashboard" style={{ padding: "96px 24px", background: "#0f0f0f", borderTop: "1px solid #1c1c1c" }}>
      <div style={{ maxWidth: 1300, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 52 }}>
          <div className="section-label" style={{ marginBottom: 14 }}>Live System</div>
          <h2 style={{ fontSize: "clamp(1.8rem, 4vw, 2.8rem)", color: "#ffffff" }}>Live Dashboard</h2>
          <p style={{ color: "#666666", marginTop: 14, fontSize: "1rem", maxWidth: 480, margin: "14px auto 0" }}>
            The full Streamlit dashboard running live — real sensor data, energy analytics, and weather-adaptive logic in action.
          </p>
        </div>

        <div style={{
          border: "1px solid #1c1c1c",
          borderRadius: 16,
          overflow: "hidden",
          background: "#0f0f0f",
        }}>
          {/* Browser chrome */}
          <div style={{
            background: "#161616",
            borderBottom: "1px solid #1c1c1c",
            padding: "10px 16px",
            display: "flex",
            alignItems: "center",
            gap: 12,
          }}>
            <div style={{ display: "flex", gap: 6 }}>
              <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#ef4444" }} />
              <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#f59e0b" }} />
              <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#84cc16" }} />
            </div>
            <div style={{
              flex: 1, background: "#0f0f0f", borderRadius: 6, padding: "5px 12px",
              fontSize: "0.74rem", color: "#555555", fontFamily: "monospace",
              border: "1px solid #1c1c1c",
            }}>
              {DASHBOARD_URL}
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "0.72rem", color: "#84cc16", fontWeight: 600, letterSpacing: "0.06em" }}>
              <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#84cc16", display: "inline-block", animation: "pulse-dot 1.6s ease-in-out infinite" }} />
              LIVE
            </div>
          </div>

          <iframe
            src={DASHBOARD_URL}
            style={{ width: "100%", height: "85vh", minHeight: 700, border: "none", display: "block" }}
            title="Smart Fan Energy Watch — Live Dashboard"
            allow="fullscreen"
          />
        </div>
      </div>
    </section>
  );
}
