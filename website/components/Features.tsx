"use client";

const FEATURES = [
  { title: "Real-Time Telemetry",    desc: "ESP32 streams temperature, power draw, and fan mode to Supabase every 10 seconds with automatic reconnection.", accent: "#84cc16" },
  { title: "Weather-Adaptive Logic", desc: "MED and HIGH thresholds are dynamically set from live outdoor temperature and daily peak via Open-Meteo API.", accent: "#22d3ee" },
  { title: "Energy Savings Analysis",desc: "Time-weighted kWh integration compares adaptive usage against a constant baseline to quantify real savings.", accent: "#f59e0b" },
  { title: "Cost Impact Estimation", desc: "Converts energy savings to dollar amounts at a configurable electricity rate in real time.", accent: "#84cc16" },
  { title: "Mode Distribution",      desc: "Donut chart breaks down how long the fan spent in each mode — OFF, LOW, MEDIUM, HIGH — over your chosen window.", accent: "#22d3ee" },
  { title: "Live Visualizations",    desc: "Temperature and power charts with mode-colored bands, threshold lines, and per-point hover tooltips.", accent: "#f59e0b" },
];

export default function Features() {
  return (
    <section id="features" style={{ padding: "96px 24px", background: "#0f0f0f", borderTop: "1px solid #1c1c1c", borderBottom: "1px solid #1c1c1c" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 64 }}>
          <div className="section-label" style={{ marginBottom: 14 }}>What It Does</div>
          <h2 style={{ fontSize: "clamp(1.8rem, 4vw, 2.8rem)", color: "#ffffff" }}>Key Features</h2>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 1, background: "#1c1c1c", borderRadius: 16, overflow: "hidden" }}>
          {FEATURES.map((f, i) => (
            <div
              key={i}
              style={{ background: "#0f0f0f", padding: "28px 26px", transition: "background 0.2s", cursor: "default", position: "relative", overflow: "hidden" }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#161616"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "#0f0f0f"; }}
            >
              <div style={{ width: 3, height: 3, borderRadius: "50%", background: f.accent, marginBottom: 18, opacity: 0.7 }} />
              <h3 style={{ fontSize: "0.95rem", color: "#ffffff", marginBottom: 10, fontFamily: "'Space Grotesk', sans-serif", fontWeight: 600 }}>{f.title}</h3>
              <p style={{ fontSize: "0.84rem", color: "#666666", lineHeight: 1.75 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
