export default function Footer() {
  return (
    <footer style={{
      borderTop: "1px solid #1c1c1c",
      padding: "36px 24px",
      maxWidth: 1100,
      margin: "0 auto",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      flexWrap: "wrap",
      gap: 12,
    }}>
      <div style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: "0.95rem", color: "#ffffff" }}>
        Smart Fan <span style={{ color: "#84cc16" }}>Energy</span> Watch
      </div>
      <div style={{ fontSize: "0.78rem", color: "#444444" }}>
        ESP32 + Supabase + Streamlit — Weather-Adaptive IoT Energy Monitor
      </div>
      <div style={{ display: "flex", gap: 6 }}>
        {[
          { name: "ESP32",     color: "#f59e0b" },
          { name: "Supabase",  color: "#84cc16" },
          { name: "Streamlit", color: "#22d3ee" },
        ].map((t) => (
          <span key={t.name} style={{
            fontSize: "0.72rem", padding: "3px 10px", borderRadius: 999,
            border: "1px solid #1c1c1c", color: "#444444",
          }}>{t.name}</span>
        ))}
      </div>
    </footer>
  );
}
