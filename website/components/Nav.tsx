'use client'
import { useState } from 'react'

const links = [
  { href: '#hero',         label: 'Overview' },
  { href: '#problem',      label: 'The Problem' },
  { href: '#approach',     label: 'What We Built' },
  { href: '#architecture', label: 'How It Works' },
  { href: '#dashboard',    label: 'Try It' },
  { href: '#faq',          label: 'FAQ' },
]

export default function Nav() {
  const [open, setOpen] = useState(false)

  return (
    <header
      className="sticky top-0 z-50 text-white"
      style={{ background: 'linear-gradient(180deg, #0f172b 0%, #12203d 100%)', boxShadow: '0 1px 0 rgba(255,255,255,0.06)' }}
    >
      <div className="site-container">
        <div className="flex items-center gap-4 min-h-[70px]">
          {/* Hamburger */}
          <button
            type="button"
            aria-expanded={open}
            aria-controls="nav-drawer"
            onClick={() => setOpen(v => !v)}
            className="w-11 h-11 rounded-full flex flex-col items-center justify-center gap-[5px] cursor-pointer border-none shrink-0 transition-colors"
            style={{ background: 'rgba(255,255,255,0.08)' }}
          >
            <span className="block w-[18px] h-[1.5px] bg-white rounded" />
            <span className="block w-[18px] h-[1.5px] bg-white rounded" />
            <span className="block w-[18px] h-[1.5px] bg-white rounded" />
            <span className="sr-only">Toggle navigation</span>
          </button>

          {/* Brand */}
          <a href="#hero" aria-label="Home" className="flex-1 flex flex-col leading-tight">
            <span className="font-bold text-[1.05rem] tracking-[-0.02em]">Weather-Adaptive</span>
            <span className="text-[0.62rem] text-white/55 font-medium tracking-wide uppercase">IoT Energy Monitor</span>
          </a>

          {/* CTA */}
          <a
            href="http://127.0.0.1:8501"
            target="_blank"
            rel="noreferrer"
            className="btn btn-green text-sm px-5 min-h-[40px]"
          >
            Live dashboard
          </a>
        </div>
      </div>

      {/* Drawer */}
      <nav id="nav-drawer" className={`nav-panel-drawer ${open ? 'is-open' : ''}`}>
        <div
          className="site-container flex flex-wrap gap-x-6 gap-y-1 pb-4 pt-1"
          style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
        >
          {links.map(l => (
            <a
              key={l.href}
              href={l.href}
              onClick={() => setOpen(false)}
              className="py-2 text-sm font-medium text-white/70 hover:text-white transition-colors"
            >
              {l.label}
            </a>
          ))}
        </div>
      </nav>
    </header>
  )
}
