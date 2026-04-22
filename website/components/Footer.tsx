export default function Footer() {
  return (
    <footer
      className="py-12"
      style={{ background: '#0f172b', borderTop: '1px solid rgba(255,255,255,0.06)' }}
    >
      <div
        className="site-container grid gap-8"
        style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}
      >
        <div>
          <a href="#hero" className="font-bold text-white text-sm block mb-2">
            Weather-Adaptive IoT Energy Monitor
          </a>
          <p className="text-slate-400 text-sm leading-relaxed">
            A fan-focused embedded and cloud prototype built with ESP32, Supabase,
            Streamlit, and Open-Meteo.
          </p>
        </div>

        <div className="flex flex-col gap-2">
          <span className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-1">Sections</span>
          {[
            ['#problem',      'The Problem'],
            ['#approach',     'What We Built'],
            ['#architecture', 'How It Works'],
            ['#scope',        'Scope'],
            ['#faq',          'FAQ'],
          ].map(([href, label]) => (
            <a key={href} href={href} className="text-slate-400 text-sm hover:text-white transition-colors">
              {label}
            </a>
          ))}
        </div>

        <div className="flex flex-col gap-2">
          <span className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-1">Code</span>
          {[
            ['http://127.0.0.1:8501',          'Open local dashboard', true],
            ['../dashboard/finalapp.py',         'View dashboard code',  false],
            ['../firmware/esp.c++',              'View firmware code',   false],
          ].map(([href, label, external]) => (
            <a
              key={String(href)}
              href={String(href)}
              target={external ? '_blank' : undefined}
              rel={external ? 'noreferrer' : undefined}
              className="text-slate-400 text-sm hover:text-white transition-colors"
            >
              {label}
            </a>
          ))}
        </div>
      </div>
    </footer>
  )
}
