export default function ArchitectureSection() {
  return (
    <section
      id="architecture"
      className="slide"
      style={{ background: 'linear-gradient(180deg,#ffffff 0%,#f9fbfd 100%)', borderTop: '1px solid rgba(191,208,223,0.4)' }}
    >
      <div className="site-container w-full">
        <div
          className="grid gap-12 items-center"
          style={{ gridTemplateColumns: 'minmax(0,1fr) minmax(320px,480px)' }}
        >
          {/* Copy */}
          <div>
            <p className="eyebrow">How It Works</p>
            <h2
              className="slide-heading mt-1"
              style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)' }}
            >
              A four-layer prototype
            </h2>
            <p className="text-slate-500 leading-relaxed mt-4" style={{ fontSize: '1.02rem' }}>
              Every layer is connected. The ESP32 gathers and publishes readings on a fixed
              cadence. Supabase stores the time-series data in a queryable table. Streamlit
              transforms that data into a live dashboard with energy analytics. Open-Meteo
              supplies outdoor weather so indoor readings are always in context.
            </p>

            <ul className="mt-6 flex flex-col gap-3">
              {[
                {
                  label: 'ESP32 firmware',
                  desc: 'Reads indoor temperature, maps to fan mode, posts estimated wattage every 10 s.',
                },
                {
                  label: 'Supabase',
                  desc: 'Stores device_id, temp_c, power_w, and fan_mode in the fan_readings table.',
                },
                {
                  label: 'Streamlit dashboard',
                  desc: 'Computes weather thresholds, rolling analytics, savings, and cost projections.',
                },
                {
                  label: 'Open-Meteo',
                  desc: 'Supplies current and peak outdoor temperature for dashboard context.',
                },
              ].map(({ label, desc }) => (
                <li key={label} className="flex gap-3 items-start text-sm leading-relaxed">
                  <span
                    className="shrink-0 mt-[3px] w-2 h-2 rounded-full"
                    style={{ background: '#1a8a68' }}
                  />
                  <span>
                    <strong className="text-slate-800">{label}:</strong>{' '}
                    <span className="text-slate-500">{desc}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Ring diagram */}
          <div className="ring-orbit" aria-hidden="true">
            <div className="ring-core">
              <span>Weather-Adaptive<br />Monitor</span>
            </div>
            <div className="ring-node ring-node-1">ESP32</div>
            <div className="ring-node ring-node-2">Supabase</div>
            <div className="ring-node ring-node-3">Streamlit</div>
            <div className="ring-node ring-node-4">Open-Meteo</div>
          </div>
        </div>
      </div>
    </section>
  )
}
