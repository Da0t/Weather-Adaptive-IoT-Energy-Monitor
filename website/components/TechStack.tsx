"use client";

const TECH = [
  { name: "ESP32",      color: "#f59e0b" },
  { name: "C++",        color: "#22d3ee" },
  { name: "Supabase",   color: "#84cc16" },
  { name: "PostgreSQL", color: "#22d3ee" },
  { name: "Python",     color: "#f59e0b" },
  { name: "Streamlit",  color: "#ef4444" },
  { name: "Plotly",     color: "#22d3ee" },
  { name: "Pandas",     color: "#84cc16" },
  { name: "Open-Meteo", color: "#f59e0b" },
  { name: "DS18B20",    color: "#888888" },
];

export default function TechStack() {
  return (
    <section style={{ padding: "72px 24px", maxWidth: 1100, margin: "0 auto", textAlign: "center" }}>
      <div className="section-label" style={{ marginBottom: 28 }}>Built With</div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
        {TECH.map((t) => (
          <span
            key={t.name}
            style={{
              fontSize: "0.82rem", fontWeight: 500,
              padding: "7px 16px", borderRadius: 999,
              background: "transparent",
              border: "1px solid #1c1c1c",
              color: "#888888",
              fontFamily: "'Space Grotesk', sans-serif",
              transition: "border-color 0.15s, color 0.15s",
              cursor: "default",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.borderColor = t.color + "55";
              (e.currentTarget as HTMLElement).style.color = t.color;
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.borderColor = "#1c1c1c";
              (e.currentTarget as HTMLElement).style.color = "#888888";
            }}
          >
            {t.name}
          </span>
        ))}
      </div>
    </section>
  );
}
