const STEPS = [
  {
    num: "01", title: "ESP32 Edge Device", color: "#f59e0b",
    desc: "DS18B20 temperature sensor reads ambient temp every 10 seconds. The ESP32 computes fan mode using weather-adaptive thresholds from Open-Meteo.",
    tags: ["C++", "DS18B20", "Open-Meteo", "Wi-Fi"],
  },
  {
    num: "02", title: "Supabase Cloud Layer", color: "#22d3ee",
    desc: "Telemetry is streamed via HTTPS POST to a Supabase PostgreSQL table. Every reading includes timestamp, temperature, power draw, and fan mode.",
    tags: ["PostgreSQL", "REST API", "Real-time", "Cloud"],
  },
  {
    num: "03", title: "Streamlit Dashboard", color: "#84cc16",
    desc: "The dashboard polls Supabase live, computes time-weighted energy usage, compares against a constant baseline, and visualizes savings in real time.",
    tags: ["Python", "Streamlit", "Plotly", "Pandas"],
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" style={{ padding: "96px 24px", maxWidth: 1100, margin: "0 auto" }}>
      <div style={{ textAlign: "center", marginBottom: 64 }}>
        <div className="section-label" style={{ marginBottom: 14 }}>Architecture</div>
        <h2 style={{ fontSize: "clamp(1.8rem, 4vw, 2.8rem)", color: "#ffffff" }}>How It Works</h2>
        <p style={{ color: "#666666", marginTop: 14, fontSize: "1rem", maxWidth: 480, margin: "14px auto 0" }}>
          Three tightly integrated layers from physical sensor to live analytics.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 1, background: "#1c1c1c", borderRadius: 16, overflow: "hidden" }}>
        {STEPS.map((step, i) => (
          <div key={i} style={{ background: "#0f0f0f", padding: "36px 32px", position: "relative" }}>
            <div style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "4rem", fontWeight: 800, color: "#ffffff", opacity: 0.04, position: "absolute", top: 12, right: 24, lineHeight: 1 }}>{step.num}</div>
            <div style={{ width: 4, height: 4, borderRadius: "50%", background: step.color, marginBottom: 20, opacity: 0.7 }} />
            <h3 style={{ fontSize: "1.1rem", color: "#ffffff", marginBottom: 12, fontFamily: "'Space Grotesk', sans-serif" }}>{step.title}</h3>
            <p style={{ fontSize: "0.87rem", color: "#666666", lineHeight: 1.75, marginBottom: 24 }}>{step.desc}</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {step.tags.map((tag) => (
                <span key={tag} style={{
                  fontSize: "0.71rem", fontWeight: 600,
                  padding: "3px 10px", borderRadius: 999,
                  background: "transparent", border: "1px solid #2a2a2a",
                  color: "#555555", letterSpacing: "0.04em",
                }}>{tag}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 10, marginTop: 28, opacity: 0.3 }}>
        <span style={{ fontSize: "0.72rem", color: "#888888", letterSpacing: "0.1em" }}>ESP32</span>
        <svg width="60" height="8" viewBox="0 0 60 8"><path d="M0 4h52M49 1l3 3-3 3" stroke="#888" strokeWidth="1.2" fill="none" strokeLinecap="round"/></svg>
        <span style={{ fontSize: "0.72rem", color: "#888888", letterSpacing: "0.1em" }}>SUPABASE</span>
        <svg width="60" height="8" viewBox="0 0 60 8"><path d="M0 4h52M49 1l3 3-3 3" stroke="#888" strokeWidth="1.2" fill="none" strokeLinecap="round"/></svg>
        <span style={{ fontSize: "0.72rem", color: "#888888", letterSpacing: "0.1em" }}>DASHBOARD</span>
      </div>
    </section>
  );
}
