export default function DashboardSection() {
  return (
    <section
      id="dashboard"
      className="slide"
      style={{ background: 'linear-gradient(135deg, #0f172b 0%, #162340 55%, #0f2540 100%)' }}
    >
      <div className="site-container w-full">
        <div style={{ maxWidth: '680px' }}>
          <p className="eyebrow" style={{ color: 'rgba(255,255,255,0.45)' }}>Try It</p>

          <h2
            className="slide-heading text-white mt-1"
            style={{ fontSize: 'clamp(2rem, 4vw, 3.4rem)' }}
          >
            Explore the live pipeline
          </h2>

          <p className="text-slate-300 leading-relaxed mt-4" style={{ fontSize: '1.05rem', maxWidth: '54ch' }}>
            Open the Streamlit dashboard to see real-time telemetry, energy comparisons,
            adaptive mode decisions, and cost projections across multiple electricity markets.
            A demo mode simulates telemetry so you can explore everything without hardware.
          </p>

          <div className="flex flex-wrap gap-4 mt-8">
            <a
              href="http://127.0.0.1:8501"
              target="_blank"
              rel="noreferrer"
              className="btn btn-white"
            >
              Open dashboard
            </a>
            <a href="#scope" className="btn btn-ghost-light">
              View scope &amp; details
            </a>
          </div>

          <div
            className="grid gap-4 mt-10"
            style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))' }}
          >
            {[
              { label: 'Demo mode available',  desc: 'Explore all analytics without hardware' },
              { label: 'Runs locally',          desc: 'Streamlit on localhost:8501' },
              { label: 'Multiple markets',      desc: 'Cost projections for US, EU, AU grids' },
            ].map(({ label, desc }) => (
              <div
                key={label}
                className="rounded-xl p-4"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}
              >
                <strong className="block text-white text-sm font-semibold">{label}</strong>
                <span className="block text-slate-400 text-xs mt-1 leading-snug">{desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
