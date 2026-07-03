import { motion } from 'framer-motion'
import Card from '../ui/Card'

export function MentorCard({ title, subtitle, footer, variant = 'default', compact = false, className = '', children, ...props }) {
  const variantClasses = {
    default: 'border-white/10 bg-slate-950/70 shadow-[0_20px_60px_rgba(0,0,0,0.32)]',
    highlight: 'border-cyan-400/20 bg-slate-900/75 shadow-[0_24px_80px_rgba(8,145,178,0.16)]',
    muted: 'border-white/5 bg-white/5 shadow-none',
  }

  return (
    <motion.div whileHover={{ y: 2 }} className={`rounded-[1.75rem] ${variantClasses[variant]} ${compact ? 'p-4' : 'p-6'} ${className}`} {...props}>
      {title && <div className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-slate-300">{title}</div>}
      {subtitle && <div className="mb-4 text-sm text-slate-400">{subtitle}</div>}
      <div className="space-y-4">{children}</div>
      {footer && <div className="mt-6 text-sm text-slate-500">{footer}</div>}
    </motion.div>
  )
}

export default MentorCard
