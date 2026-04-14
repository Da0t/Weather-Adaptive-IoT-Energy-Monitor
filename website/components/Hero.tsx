"use client";

export default function Hero() {
  return (
    <section style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden",
      background: "#0f0f0f",
      paddingTop: "140px",
      paddingBottom: "100px",
    }}>
      {/* Subtle radial glow — dashboard colors as background hints */}
      <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        <div style={{ position: "absolute", top: "-10%", left: "-5%", width: 600, height: 600, borderRadius: "50%", background: "radial-gradient(circle, rgba(132,204,22,0.06) 0%, transparent 70%)" }} />
        <div style={{ position: "absolute", top: "20%", right: "-10%", width: 500, height: 500, borderRadius: "50%", background: "radial-gradient(circle, rgba(34,211,238,0.05) 0%, transparent 70%)" }} />
        <div style={{ position: "absolute", bottom: "10%", left: "30%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle, rgba(245,158,11,0.04) 0%, transparent 70%)" }} />
      </div>

      {/* Subtle grid */}
      <div style={{
        position: "absolute", inset: 0, opacity: 0.03,
        backgroundImage: "linear-gradient(#ffffff 1px, transparent 1px), linear-gradient(90deg, #ffffff 1px, transparent 1px)",
        backgroundSize: "80px 80px",
        pointerEvents: "none",
      }} />

      <div style={{ maxWidth: 860, margin: "0 auto", padding: "0 24px", textAlign: "center", position: "relative", zIndex: 1 }}>

        {/* Status pill */}
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 8,
          border: "1px solid #1c1c1c",
          borderRadius: 999, padding: "6px 16px", marginBottom: 40,
          fontSize: "0.75rem", fontWeight: 600, color: "#888888", letterSpacing: "0.08em",
          background: "#161616",
        }}>
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#84cc16", display: "inline-block", animation: "pulse-dot 1.6s ease-in-out infinite" }} />
          LIVE SYSTEM ACTIVE
        </div>

        <h1 style={{
          fontSize: "clamp(3rem, 8vw, 6rem)",
          fontFamily: "'Space Grotesk', sans-serif",
          fontWeight: 800,
          lineHeight: 1.0,
          letterSpacing: "-0.04em",
          color: "#ffffff",
          marginBottom: 16,
        }}>
          Smart Fan<br />
          <span className="gradient-text">Energy</span> Watch
        </h1>

        <p style={{
          fontSize: "clamp(0.95rem, 2vw, 1.15rem)",
          color: "#666666",
          lineHeight: 1.75,
          maxWidth: 520,
          margin: "24px auto 44px",
        }}>
          Real-time IoT energy monitoring powered by ESP32, Supabase &amp; weather-adaptive intelligence.
        </p>

        <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
          <a href="#dashboard" className="btn-primary">
            View Live Dashboard
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/></svg>
          </a>
          <a href="#how-it-works" className="btn-outline">
            How It Works
          </a>
        </div>

        {/* Stat strip */}
        <div style={{ display: "flex", justifyContent: "center", gap: 48, marginTop: 80, flexWrap: "wrap", borderTop: "1px solid #1c1c1c", paddingTop: 40 }}>
          {[
            { val: "10s",  label: "Update Interval",  dot: "#84cc16" },
            { val: "4",    label: "Fan Modes",         dot: "#22d3ee" },
            { val: "3",    label: "System Layers",     dot: "#f59e0b" },
            { val: "Live", label: "Weather Sync",      dot: "#84cc16" },
          ].map((s) => (
            <div key={s.label} style={{ textAlign: "center" }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
                <div style={{ width: 4, height: 4, borderRadius: "50%", background: s.dot, opacity: 0.7, flexShrink: 0 }} />
                <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: "1.8rem", color: "#ffffff" }}>{s.val}</span>
              </div>
              <div style={{ fontSize: "0.72rem", color: "#444444", marginTop: 4, letterSpacing: "0.06em", textTransform: "uppercase" }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
