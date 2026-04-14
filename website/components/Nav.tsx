"use client";
import { useEffect, useState } from "react";

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
      style={scrolled ? { background: "rgba(15,15,15,0.92)", backdropFilter: "blur(14px)", borderBottom: "1px solid #1c1c1c" } : {}}
    >
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between", height: 64 }}>
        <div style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: "1rem", color: "#ffffff" }}>
          Smart Fan <span style={{ color: "#84cc16" }}>Energy</span> Watch
        </div>
        <div className="hidden md:flex items-center gap-8">
          {["How It Works", "Features", "Dashboard"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase().replace(/ /g, "-")}`}
              style={{ fontSize: "0.88rem", color: "#666666", fontWeight: 500, textDecoration: "none", transition: "color 0.15s" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#666666")}
            >
              {item}
            </a>
          ))}
        </div>
        <a href="#dashboard" className="btn-primary" style={{ padding: "8px 20px", fontSize: "0.84rem" }}>
          View Live
        </a>
      </div>
    </nav>
  );
}
