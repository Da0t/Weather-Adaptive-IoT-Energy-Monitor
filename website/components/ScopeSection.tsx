export default function ScopeSection() {
  return (
    <section
      id="scope"
      className="slide"
      style={{ background: '#ffffff', borderTop: '1px solid rgba(191,208,223,0.4)' }}
    >
      <div className="site-container w-full">
        <div
          className="grid gap-10 items-start"
          style={{ gridTemplateColumns: 'minmax(0,1.2fr) minmax(260px,380px)' }}
        >
          {/* Left — callouts */}
          <div>
            <p className="eyebrow">Current Scope</p>
            <h2
              className="slide-heading mt-1"
              style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)', maxWidth: '20ch' }}
            >
              What the prototype is and what it is not
            </h2>

            <div className="flex flex-col gap-4 mt-8">
              <div
                className="callout-is content-card p-5"
                style={{ borderRadius: '18px' }}
              >
                <h3 className="font-bold text-[0.95rem] text-slate-800 mb-1">What it is</h3>
                <p className="text-slate-500 text-sm leading-relaxed">
                  A working firmware-to-dashboard pipeline for a fan-focused case study, with
                  live telemetry, outdoor weather framing, and energy comparison views. All
                  layers are connected and producing real data.
                </p>
              </div>

              <div
                className="callout-not content-card p-5"
                style={{ borderRadius: '18px' }}
              >
                <h3 className="font-bold text-[0.95rem] text-slate-800 mb-1">What it is not yet</h3>
                <p className="text-slate-500 text-sm leading-relaxed">
                  A direct weather-actuated hardware controller. The ESP32 still uses fixed
                  indoor temperature bands rather than live outdoor weather on-device. Actuation
                  (relay, PWM, or motor control) is not yet implemented.
                </p>
              </div>

              <div
                className="callout-next content-card p-5"
                style={{ borderRadius: '18px' }}
              >
                <h3 className="font-bold text-[0.95rem] text-slate-800 mb-1">What comes next</h3>
                <p className="text-slate-500 text-sm leading-relaxed">
                  Relay or PWM-based fan control, hysteresis to prevent rapid mode oscillation,
                  multi-device support, direct power measurement (replacing estimated wattage),
                  and on-device weather-aware threshold adjustment.
                </p>
              </div>
            </div>
          </div>

          {/* Right — detail card */}
          <aside className="content-card p-6" style={{ borderRadius: '24px' }}>
            <div className="flex items-center justify-between mb-5">
              <span
                className="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full"
                style={{ background: 'rgba(26,138,104,0.1)', color: '#1a8a68' }}
              >
                Prototype details
              </span>
              <span
                className="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full"
                style={{ background: 'rgba(26,138,104,0.08)', color: '#1a8a68' }}
              >
                Live-ready
              </span>
            </div>

            {[
              ['Sensor',          'DS18B20'],
              ['Microcontroller', 'ESP32'],
              ['Backend',         'Supabase'],
              ['Analytics',       'Streamlit + Plotly'],
              ['Weather API',     'Open-Meteo'],
              ['Power data',      'Estimated by mode'],
              ['Telemetry',       'Every 10 seconds'],
            ].map(([k, v]) => (
              <div
                key={k}
                className="flex items-center justify-between py-3 text-sm"
                style={{ borderBottom: '1px solid #eef2f7' }}
              >
                <span className="text-slate-500">{k}</span>
                <strong className="text-slate-800">{v}</strong>
              </div>
            ))}

            {/* Mini chart decoration */}
            <div className="mt-5 rounded-xl overflow-hidden" style={{ height: '48px', background: '#f8fafc' }}>
              <div className="h-1 w-full" style={{ background: 'linear-gradient(90deg,#1a8a68,#38bdf8,#615fff)', opacity: 0.5 }} />
              <div className="flex items-end gap-1 px-3 pb-2 pt-1 h-full">
                {[30, 55, 40, 70, 50, 80, 60, 75, 45, 65].map((h, i) => (
                  <div
                    key={i}
                    className="flex-1 rounded-sm"
                    style={{ height: `${h}%`, background: 'rgba(26,138,104,0.25)' }}
                  />
                ))}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>
  )
}
