export default function ProblemSection() {
  return (
    <section
      id="problem"
      className="slide"
      style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)', borderTop: '1px solid rgba(191,208,223,0.4)' }}
    >
      <div className="site-container w-full">
        <p className="eyebrow">The Problem</p>

        <h2
          className="slide-heading"
          style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)', maxWidth: '22ch' }}
        >
          Cooling demand is rising. The tools to manage it aren&rsquo;t keeping up.
        </h2>

        <p
          className="mt-4 text-slate-500 leading-relaxed"
          style={{ maxWidth: '64ch', fontSize: '1.02rem' }}
        >
          The environmental motivation for this project came directly from the data. These three
          sources &mdash; an IEA report, a NERC grid assessment, and S&amp;P Global adoption research &mdash;
          made it clear that cooling energy is one of the most impactful, and most neglected,
          targets for emissions reduction. They shaped every design decision we made.
        </p>

        <div className="grid gap-6 mt-10" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>

          {/* Card 1 — IEA */}
          <article className="content-card p-7 flex flex-col">
            <span
              className="text-xs font-bold uppercase tracking-widest"
              style={{ color: '#64748b' }}
            >
              IEA &middot; 14 May 2018
            </span>

            <div
              className="slide-heading mt-3 mb-1"
              style={{ fontSize: '2.4rem', color: '#1a8a68', fontFamily: 'var(--font-space-grotesk, sans-serif)' }}
            >
              3&times;
            </div>
            <h3 className="font-bold text-[1.05rem] text-navy leading-snug">
              Cooling demand is the fastest-growing electricity end-use
            </h3>

            <p className="text-slate-500 text-sm leading-relaxed mt-3 flex-1">
              The IEA projects energy demand for space cooling could triple by 2050, reaching
              6,200&nbsp;TWh&nbsp;/&nbsp;year without stronger efficiency measures. Cooling
              already accounts for nearly{' '}
              <strong className="text-slate-700">10% of global electricity</strong>, a share
              growing in every major region. The hottest days produce demand spikes that push
              grids already running near capacity to their limits.
            </p>

            <p className="text-slate-400 text-xs leading-relaxed mt-3 italic">
              This is the macro trend our prototype tries to make measurable at the micro
              scale: one device, one room, one fan &mdash; but the data pattern scales.
            </p>

            <a
              href="https://www.iea.org/reports/the-future-of-cooling/"
              target="_blank"
              rel="noreferrer"
              className="mt-5 text-sm font-semibold self-start transition-colors"
              style={{ color: '#1a8a68' }}
            >
              View source &rarr;
            </a>
          </article>

          {/* Card 2 — NERC */}
          <article className="content-card p-7 flex flex-col">
            <span
              className="text-xs font-bold uppercase tracking-widest"
              style={{ color: '#64748b' }}
            >
              NERC &middot; May 2025
            </span>

            <div
              className="slide-heading mt-3 mb-1"
              style={{ fontSize: '2.4rem', color: '#1a8a68', fontFamily: 'var(--font-space-grotesk, sans-serif)' }}
            >
              +10 GW
            </div>
            <h3 className="font-bold text-[1.05rem] text-navy leading-snug">
              Peak demand is rising faster than planners can keep up
            </h3>

            <p className="text-slate-500 text-sm leading-relaxed mt-3 flex-1">
              NERC&rsquo;s 2025 Summer Reliability Assessment found aggregated peak demand
              across 23 assessment areas grew by{' '}
              <strong className="text-slate-700">more than 10&nbsp;GW in a single year</strong>.
              That rate of growth creates increasing reliability risk at the exact moments
              cooling demand peaks. If smart HVAC controls reduced peak load by just 5&ndash;10%,
              that represents several gigawatts of avoided demand &mdash; without building a
              single new power plant.
            </p>

            <p className="text-slate-400 text-xs leading-relaxed mt-3 italic">
              Our prototype tracks real-time fan modes and estimated wattage &mdash; exactly
              the kind of per-device signal a demand response system would need.
            </p>

            <a
              href="https://www.nerc.com/globalassets/programs/rapa/ra/nerc_sra_2025.pdf"
              target="_blank"
              rel="noreferrer"
              className="mt-5 text-sm font-semibold self-start transition-colors"
              style={{ color: '#1a8a68' }}
            >
              View source &rarr;
            </a>
          </article>

          {/* Card 3 — Utility Dive */}
          <article className="content-card p-7 flex flex-col">
            <span
              className="text-xs font-bold uppercase tracking-widest"
              style={{ color: '#64748b' }}
            >
              Utility Dive &middot; 31 Aug. 2022
            </span>

            <div
              className="slide-heading mt-3 mb-1"
              style={{ fontSize: '2.4rem', color: '#1a8a68', fontFamily: 'var(--font-space-grotesk, sans-serif)' }}
            >
              &lt;20%
            </div>
            <h3 className="font-bold text-[1.05rem] text-navy leading-snug">
              Smart controls exist, but most buildings don&rsquo;t use them
            </h3>

            <p className="text-slate-500 text-sm leading-relaxed mt-3 flex-1">
              S&amp;P Global research found that smart thermostat adoption remains{' '}
              <strong className="text-slate-700">below 20% in eligible US households</strong>{' '}
              despite being technically available for over a decade. The barriers are not
              hardware: the devices work, the APIs exist, and the documented energy savings
              are real. The gap is in <em>visibility</em> &mdash; most people have no data on
              what their cooling equipment is doing or what it costs per hour.
            </p>

            <p className="text-slate-400 text-xs leading-relaxed mt-3 italic">
              Our system attempts to close that visibility gap at the sensor level, without
              requiring a full smart-home installation.
            </p>

            <a
              href="https://www.utilitydive.com/news/smart-thermostats-us-slow-adoption-misses-energy-savings/630901/"
              target="_blank"
              rel="noreferrer"
              className="mt-5 text-sm font-semibold self-start transition-colors"
              style={{ color: '#1a8a68' }}
            >
              View source &rarr;
            </a>
          </article>

        </div>
      </div>
    </section>
  )
}
