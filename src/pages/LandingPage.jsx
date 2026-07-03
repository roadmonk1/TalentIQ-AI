import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion'
import { useEffect, useState } from 'react'
import { ArrowRight, BrainCircuit, BriefcaseBusiness, Sparkles, Mic, ScrollText } from 'lucide-react'
import { Reveal } from '../components/Reveal'

const pillars = [
  {
    title: 'AI Career OS',
    description: 'Turn your experience into a dynamic operating system for growth, interviews, and opportunities.',
    icon: BrainCircuit,
  },
  {
    title: 'Recruiter-grade insights',
    description: 'Surface blind spots in resumes, portfolios, and communication before the market does.',
    icon: BriefcaseBusiness,
  },
  {
    title: 'Interview readiness',
    description: 'Practice with mock, voice, and coding interviews that feel closer to real hiring loops.',
    icon: Mic,
  },
]

export function LandingPage() {
  const [atsScore, setAtsScore] = useState(0)
  const [visibleCards, setVisibleCards] = useState(false)

  const springScore = useSpring(atsScore, { stiffness: 90, damping: 20, mass: 0.8 })
  const displayScore = useTransform(springScore, (value) => Math.round(value))

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setAtsScore(92)
      setVisibleCards(true)
    }, 300)

    return () => window.clearTimeout(timer)
  }, [])

  return (
    <section className="mx-auto flex max-w-7xl flex-col gap-16 px-6 pb-24 pt-6 sm:px-8 lg:px-10 lg:pb-32">
      <div className="grid items-center gap-12 lg:grid-cols-[1.1fr_0.9fr]">
        <Reveal className="max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, ease: [0.16, 1, 0.3, 1] }}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200 shadow-[0_0_30px_rgba(34,211,238,0.12)]"
          >
            <Sparkles className="h-4 w-4" />
            The AI Career Operating System for ambitious builders
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.08, ease: [0.16, 1, 0.3, 1] }}
            className="text-5xl font-semibold tracking-[-0.04em] text-white sm:text-6xl lg:text-7xl"
          >
            Own your next move with <span className="text-cyan-300">TalentIQ AI</span>.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.16, ease: [0.16, 1, 0.3, 1] }}
            className="mt-6 max-w-xl text-lg leading-8 text-slate-300 sm:text-xl"
          >
            From resume intelligence to recruiter-ready positioning, TalentIQ helps people turn ambition into a measurable career edge.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.24, ease: [0.16, 1, 0.3, 1] }}
            className="mt-8 flex flex-col gap-3 sm:flex-row"
          >
            <a href="/auth" className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-5 py-3 font-medium text-slate-950 transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_18px_50px_rgba(255,255,255,0.16)]">
              Start free assessment
              <ArrowRight className="h-4 w-4" />
            </a>
            <a href="#platform" className="inline-flex items-center justify-center gap-2 rounded-full border border-white/15 bg-white/10 px-5 py-3 font-medium text-slate-200 backdrop-blur-xl transition duration-300 hover:-translate-y-0.5 hover:bg-white/20 hover:shadow-[0_12px_40px_rgba(34,211,238,0.08)]">
              Explore platform
            </a>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.32, ease: [0.16, 1, 0.3, 1] }}
            className="mt-10 flex flex-wrap gap-4 text-sm text-slate-400"
          >
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2 transition hover:border-cyan-400/30 hover:text-slate-200">ATS score intelligence</span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2 transition hover:border-cyan-400/30 hover:text-slate-200">Career roadmaps</span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2 transition hover:border-cyan-400/30 hover:text-slate-200">Recruiter dashboard</span>
          </motion.div>
        </Reveal>

        <motion.div
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.85, ease: [0.16, 1, 0.3, 1], delay: 0.12 }}
          className="relative rounded-[2rem] border border-white/10 bg-slate-950/60 p-6 shadow-[0_0_80px_rgba(14,165,233,0.16)] backdrop-blur-2xl"
        >
          <motion.div
            animate={{ y: [0, -6, 0], rotate: [0, 0.5, 0] }}
            transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
            className="absolute right-6 top-6 h-20 w-20 rounded-full bg-cyan-400/10 blur-3xl"
          />
          <div className="relative rounded-[1.5rem] border border-cyan-400/20 bg-gradient-to-br from-cyan-500/15 via-slate-900/80 to-violet-500/15 p-6">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-sm text-cyan-200">Career intelligence preview</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Your growth engine</h2>
              </div>
              <motion.div
                animate={{ scale: [1, 1.04, 1] }}
                transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}
                className="rounded-full border border-white/10 bg-white/10 p-2"
              >
                <ScrollText className="h-5 w-5 text-cyan-200" />
              </motion.div>
            </div>

            <div className="mb-5 rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
                <span>ATS score</span>
                <motion.span className="font-semibold text-cyan-200">{displayScore}</motion.span>
              </div>
              <div className="h-2 rounded-full bg-white/10">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${atsScore}%` }}
                  transition={{ duration: 1.1, ease: [0.16, 1, 0.3, 1] }}
                  className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-violet-500"
                />
              </div>
            </div>

            <div className="space-y-3">
              {[
                ['Resume analysis', '92/100 ATS readiness', 'bg-cyan-400/10'],
                ['Skill gaps', '4 growth areas identified', 'bg-violet-400/10'],
                ['Interview prep', 'Voice session ready', 'bg-emerald-400/10'],
              ].map(([label, value, tint], index) => (
                <motion.div
                  key={label}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: visibleCards ? 1 : 0, y: visibleCards ? 0 : 12 }}
                  transition={{ duration: 0.5, delay: 0.15 + index * 0.12 }}
                  className={`flex items-center justify-between rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 ${tint}`}
                >
                  <span className="text-slate-300">{label}</span>
                  <span className="font-medium text-white">{value}</span>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.35 }}
              className="mt-4 flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-2 text-sm text-emerald-200"
            >
              <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-emerald-300" />
              Recruiter signal detected
            </motion.div>
          </div>
        </motion.div>
      </div>

      <div id="platform" className="grid gap-6 lg:grid-cols-3">
        {pillars.map((pillar, index) => {
          const Icon = pillar.icon
          return (
            <Reveal key={pillar.title} delay={0.06 * index}>
              <motion.article
                whileHover={{ y: -6, scale: 1.01, boxShadow: '0 20px 60px rgba(34, 211, 238, 0.12)' }}
                transition={{ type: 'spring', stiffness: 220, damping: 20 }}
                className="rounded-[1.75rem] border border-white/10 bg-white/8 p-6 backdrop-blur-xl"
              >
                <motion.div
                  whileHover={{ rotate: 6, scale: 1.06 }}
                  transition={{ type: 'spring', stiffness: 260, damping: 16 }}
                  className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200"
                >
                  <Icon className="h-5 w-5" />
                </motion.div>
                <h3 className="text-xl font-semibold text-white">{pillar.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-400">{pillar.description}</p>
              </motion.article>
            </Reveal>
          )
        })}
      </div>
    </section>
  )
}
