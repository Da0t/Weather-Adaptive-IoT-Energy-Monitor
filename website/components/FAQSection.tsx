'use client'

const faqs = [
  {
    q: 'Does the ESP32 currently change the fan based on live outdoor weather?',
    a: 'Not yet. The firmware uses fixed indoor temperature bands to assign a mode (OFF / LOW / MED / HIGH). Live outdoor weather is fetched in the Streamlit dashboard for context and comparison logic — it does not flow back to the device. On-device weather-aware actuation is the next planned step.',
  },
  {
    q: 'Is the power value directly measured from the hardware?',
    a: 'No. Each fan mode maps to a fixed estimated watt value in the firmware. This keeps the prototype simple and avoids the need for inline power measurement hardware, while still letting the dashboard compute meaningful comparative energy and cost metrics.',
  },
  {
    q: 'Can I explore the dashboard without an ESP32 connected?',
    a: 'Yes. The Streamlit dashboard includes a demo mode that simulates a realistic stream of telemetry, so you can explore the analytics, energy comparisons, mode distribution charts, and cost projections without any physical hardware.',
  },
  {
    q: 'Why a fan and not a larger appliance first?',
    a: 'The fan makes the full sensing-to-cloud-to-dashboard pipeline easier to demonstrate cleanly. It draws enough wattage to produce meaningful energy comparisons, has well-defined operating modes, and is present in almost every indoor space — making the case study broadly relatable before expanding to more complex devices.',
  },
  {
    q: 'How accurate are the energy and cost estimates?',
    a: 'The kWh figures are time-weighted calculations using the estimated wattage per mode and the actual elapsed time in each mode from real telemetry. They are accurate relative to each other and to the simulated baseline — but they are not a substitute for direct measurement with a clamp meter or smart plug. The comparison is what matters: adaptive vs. fixed.',
  },
  {
    q: 'What electricity markets are used for cost projections?',
    a: 'The dashboard includes rate presets for California, Texas, the UK, EU average, Germany, and Australia, sourced from EIA, Ofgem, Eurostat, and AEMC 2024 data. You can also enter a custom rate per kWh to match your local tariff.',
  },
]

export default function FAQSection() {
  return (
    <section
      id="faq"
      className="slide"
      style={{
        background: 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)',
        borderTop: '1px solid rgba(191,208,223,0.4)',
      }}
    >
      <div className="site-container w-full">
        <p className="eyebrow">FAQ</p>

        <h2
          className="slide-heading"
          style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)', maxWidth: '20ch' }}
        >
          Common questions about the prototype
        </h2>

        <div className="mt-10 flex flex-col" style={{ maxWidth: '760px' }}>
          {faqs.map(({ q, a }) => (
            <details
              key={q}
              className="group"
              style={{ borderBottom: '1px solid rgba(191,208,223,0.55)' }}
            >
              <summary
                className="flex items-center justify-between gap-4 py-5 cursor-pointer list-none font-semibold text-slate-800 text-[0.97rem] leading-snug select-none"
                style={{ outline: 'none' }}
              >
                <span>{q}</span>
                {/* Chevron */}
                <svg
                  viewBox="0 0 20 20"
                  className="w-5 h-5 shrink-0 text-slate-400 transition-transform duration-200 group-open:rotate-180"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M5 8l5 5 5-5" />
                </svg>
              </summary>

              <p
                className="text-slate-500 text-sm leading-relaxed pb-5"
                style={{ maxWidth: '68ch' }}
              >
                {a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  )
}
