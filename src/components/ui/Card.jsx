import { motion } from 'framer-motion'

export function Card({ children, className = '', title, footer, ...props }) {
  return (
    <motion.article
      whileHover={{ y: -6 }}
      transition={{ type: 'spring', stiffness: 220, damping: 20 }}
      className={`rounded-[1.25rem] border border-white/8 bg-slate-900/60 p-4 ${className}`}
      {...props}
    >
      {title && <div className="mb-3 text-sm font-medium text-slate-300">{title}</div>}
      <div>{children}</div>
      {footer && <div className="mt-4 text-sm text-slate-400">{footer}</div>}
    </motion.article>
  )
}

export default Card
