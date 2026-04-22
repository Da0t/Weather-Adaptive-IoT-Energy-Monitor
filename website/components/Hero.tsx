'use client'
import { Waves } from '@/components/ui/wave-background'

export default function Hero() {
  return (
    <section
      id="hero"
      className="slide relative overflow-hidden"
      style={{ background: '#0c1525' }}
    >
      {/* Wave animation fills the entire section */}
      <Waves
        strokeColor="rgba(148, 163, 184, 0.35)"
        backgroundColor="#0c1525"
        pointerSize={0.6}
      />

      {/* Content rendered above the wave */}
      <div className="site-container relative z-10 w-full">
        <div style={{ maxWidth: '780px' }}>
          <p className="eyebrow" style={{ color: '#34d399' }}>
            IoT Energy Research &middot; Prototype
          </p>

          <h1
            className="slide-heading text-white mt-1 mb-6"
            style={{ fontSize: 'clamp(2.6rem, 5vw, 4.8rem)', maxWidth: '16ch' }}
          >
            Weather-Adaptive IoT Energy Monitor
          </h1>

          <p
            className="text-slate-300 leading-relaxed"
            style={{ fontSize: '1.08rem', maxWidth: '58ch' }}
          >
            Energy used by cooling systems is one of the fastest-growing contributors to
            grid strain &mdash; and most of it goes completely unmonitored. We built this
            prototype to show that smarter, data-driven device control can make a real
            difference: less wasted energy, lower emissions, and a measurable step toward
            more sustainable buildings.
          </p>

          <div className="flex flex-wrap gap-4 mt-8">
            <a href="#problem" className="btn btn-green">
              See the problem
            </a>
            <a
              href="http://127.0.0.1:8501"
              target="_blank"
              rel="noreferrer"
              className="btn btn-ghost-light"
            >
              Open dashboard
            </a>
          </div>

        </div>
      </div>
    </section>
  )
}
