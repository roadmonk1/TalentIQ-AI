import { useEffect, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { motion, useReducedMotion } from 'framer-motion'
import { Sparkles, Menu, ArrowRight } from 'lucide-react'

export function Layout({ children }) {
  const [scrolled, setScrolled] = useState(false)
  const prefersReducedMotion = useReducedMotion()

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-[radial-gradient(circle_at_top_left,_rgba(99,102,241,0.16),_transparent_35%),radial-gradient(circle_at_80%_20%,_rgba(56,189,248,0.14),_transparent_30%),linear-gradient(135deg,_#060816_0%,_#0b1120_45%,_#030712_100%)] text-slate-100">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute left-[-10%] top-[-12%] h-72 w-72 rounded-full bg-cyan-400/15 blur-[120px]" />
        <div className="absolute right-[-8%] top-10 h-80 w-80 rounded-full bg-violet-500/15 blur-[120px]" />
        <div className="absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-sky-500/10 blur-[120px]" />
      </div>

      <motion.header
        initial={prefersReducedMotion ? false : { y: -12, opacity: 0 }}
        animate={prefersReducedMotion ? { y: 0, opacity: 1 } : { y: 0, opacity: 1 }}
        className={`sticky top-0 z-50 mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-4 backdrop-blur-xl transition-all duration-300 sm:px-8 lg:px-10 ${scrolled ? 'bg-slate-950/40 shadow-[0_10px_40px_rgba(2,6,23,0.3)]' : 'bg-transparent'}`}
      >
        <Link to="/" className="flex items-center gap-3 text-sm font-semibold uppercase tracking-[0.24em] text-slate-200 transition hover:text-white">
          <span className="flex h-10 w-10 items-center justify-center rounded-2xl border border-white/15 bg-white/10 shadow-[0_0_40px_rgba(99,102,241,0.18)] backdrop-blur-xl transition-transform duration-300 hover:scale-105">
            <Sparkles className="h-5 w-5 text-cyan-300" />
          </span>
          TalentIQ AI
        </Link>
        <nav className="hidden items-center gap-7 text-sm text-slate-300 md:flex">
          <NavLink to="/about" className={({ isActive }) => `transition duration-300 hover:text-white ${isActive ? 'text-white' : ''}`}>
            About
          </NavLink>
          <NavLink to="/auth" className={({ isActive }) => `transition duration-300 hover:text-white ${isActive ? 'text-white' : ''}`}>
            Sign in
          </NavLink>
          <Link to="/auth" className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 font-medium text-cyan-200 transition duration-300 hover:-translate-y-0.5 hover:bg-cyan-400/20 hover:shadow-[0_0_30px_rgba(34,211,238,0.15)]">
            Join waitlist
            <ArrowRight className="h-4 w-4" />
          </Link>
        </nav>
        <button className="rounded-full border border-white/15 bg-white/10 p-2 text-slate-200 transition hover:bg-white/15 md:hidden" aria-label="Open menu">
          <Menu className="h-5 w-5" />
        </button>
      </motion.header>

      <main>{children}</main>
    </div>
  )
}
