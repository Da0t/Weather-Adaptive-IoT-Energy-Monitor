export default function ApproachSection() {
  return (
    <section
      id="approach"
      className="slide"
      style={{ background: '#ffffff', borderTop: '1px solid rgba(191,208,223,0.4)' }}
    >
      <div className="site-container w-full">
        <p className="eyebrow">What We Built</p>

        <h2
          className="slide-heading"
          style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)', maxWidth: '22ch' }}
        >
          A sensor-to-dashboard pipeline for adaptive energy monitoring
        </h2>

        <p
          className="mt-4 text-slate-500 leading-relaxed"
          style={{ maxWidth: '64ch', fontSize: '1.02rem' }}
        >
          We wanted to do more than cite statistics &mdash; we wanted to demonstrate that smarter
          device control is achievable with low-cost, accessible hardware. The system captures
          real temperature data, makes adaptive mode decisions, and makes the energy impact
          visible in a live dashboard. The goal was always environmental: show the savings,
          make them measurable, and make the case that this approach can scale.
        </p>

        <div className="grid gap-6 mt-10" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>

          {/* Card 1 — ESP32 */}
          <article className="content-card p-7 flex flex-col gap-3">
            <div
              className="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0"
              style={{ background: 'rgba(26,138,104,0.1)' }}
            >
              <svg viewBox="0 0 48 48" className="w-6 h-6" fill="none" stroke="#1a8a68" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <rect x="13" y="7" width="22" height="34" rx="6"/>
                <circle cx="24" cy="34" r="2.5"/>
                <path d="M19 14h10"/>
              </svg>
            </div>

            <div>
              <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Edge layer</div>
              <h3 className="font-bold text-[1.05rem] leading-snug">ESP32 embedded telemetry</h3>
            </div>

            <p className="text-slate-500 text-sm leading-relaxed flex-1">
              The ESP32 reads temperature from a DS18B20 sensor every{' '}
              <strong className="text-slate-700">10 seconds</strong>, applies a threshold
              function to assign one of four fan modes (OFF / LOW / MED / HIGH), and
              calculates estimated wattage for each mode. It posts a structured JSON payload
              to Supabase via HTTP &mdash; making the firmware stateless and the cloud the
              single source of truth.
            </p>

            <div
              className="rounded-xl p-3 text-xs text-slate-500 leading-relaxed"
              style={{ background: '#f8fafc', border: '1px solid #d9e2ec' }}
            >
              <strong className="text-slate-700">Design decision:</strong> Mode mapping lives
              in firmware to keep it simple. All analytics and threshold adjustments happen
              in the cloud, enabling iteration without reflashing hardware.
            </div>
          </article>

          {/* Card 2 — Weather + Cloud */}
          <article className="content-card p-7 flex flex-col gap-3">
            <div
              className="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0"
              style={{ background: 'rgba(26,138,104,0.1)' }}
            >
              <svg viewBox="0 0 48 48" className="w-6 h-6" fill="none" stroke="#1a8a68" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M10 30c0-5.5 4.5-10 10-10 1.3 0 2.5.2 3.7.7A10.5 10.5 0 0 1 43 26.5"/>
                <path d="M13 34h22"/><path d="M17 39h14"/>
                <path d="M17 11l2.2 2.2"/><path d="M31 11l-2.2 2.2"/>
              </svg>
            </div>

            <div>
              <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Context layer</div>
              <h3 className="font-bold text-[1.05rem] leading-snug">Supabase storage + live weather</h3>
            </div>

            <p className="text-slate-500 text-sm leading-relaxed flex-1">
              Supabase stores the full time-series of{' '}
              <code>device_id</code>, <code>temp_c</code>, <code>power_w</code>, and{' '}
              <code>fan_mode</code> in the <code>fan_readings</code> table. The Streamlit
              dashboard fetches current and forecast outdoor temperature from{' '}
              <strong className="text-slate-700">Open-Meteo</strong> on each load. Without
              outdoor context, indoor temperature is ambiguous: 73&deg;F indoors means
              something different depending on whether it&rsquo;s 55&deg;F or 90&deg;F outside.
            </p>

            <div
              className="rounded-xl p-3 text-xs text-slate-500 leading-relaxed"
              style={{ background: '#f8fafc', border: '1px solid #d9e2ec' }}
            >
              <strong className="text-slate-700">Design decision:</strong> Weather fetching
              sits in the dashboard, not the firmware, so threshold logic can be updated
              without any hardware changes.
            </div>
          </article>

          {/* Card 3 — Streamlit */}
          <article className="content-card p-7 flex flex-col gap-3">
            <div
              className="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0"
              style={{ background: 'rgba(26,138,104,0.1)' }}
            >
              <svg viewBox="0 0 48 48" className="w-6 h-6" fill="none" stroke="#1a8a68" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M11 33l7-7 6 5 12-14"/>
                <path d="M29 17h7v7"/>
                <path d="M9 39h30"/>
              </svg>
            </div>

            <div>
              <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Visibility layer</div>
              <h3 className="font-bold text-[1.05rem] leading-snug">Streamlit energy analytics</h3>
            </div>

            <p className="text-slate-500 text-sm leading-relaxed flex-1">
              Streamlit turns raw telemetry into structured outputs: time-weighted kWh per
              mode, cost estimates across electricity markets, and{' '}
              <strong className="text-slate-700">baseline comparisons</strong> against
              simulated always-on operation. The baseline is the core contribution &mdash; it
              shows what the same period would have cost if the fan ran at a fixed mode,
              making adaptive savings directly measurable from real sensor data.
            </p>

            <div
              className="rounded-xl p-3 text-xs text-slate-500 leading-relaxed"
              style={{ background: '#f8fafc', border: '1px solid #d9e2ec' }}
            >
              <strong className="text-slate-700">What we observed:</strong> In testing,
              adaptive mode decisions reduced estimated energy use by ~14% vs a fixed MEDIUM
              baseline. Mode transitions invisible without telemetry were captured in full.
            </div>
          </article>

        </div>

        {/* Observed data strip */}
        <div
          className="grid gap-4 mt-8"
          style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))' }}
        >
          {[
            { value: '~14%', label: 'Energy reduction vs fixed-mode baseline' },
            { value: '4',    label: 'Fan modes captured (OFF / LOW / MED / HIGH)' },
            { value: '10s',  label: 'Real-time telemetry cadence' },
            { value: '4',    label: 'Stack layers (ESP32 → Supabase → Streamlit → Open-Meteo)' },
          ].map(({ value, label }) => (
            <div
              key={value + label}
              className="rounded-2xl p-4"
              style={{ background: 'rgba(26,138,104,0.06)', border: '1px solid rgba(26,138,104,0.14)' }}
            >
              <div
                className="slide-heading mb-1"
                style={{ fontSize: '1.7rem', color: '#1a8a68', fontFamily: 'var(--font-space-grotesk, sans-serif)' }}
              >
                {value}
              </div>
              <div className="text-xs text-slate-500 leading-snug">{label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
