export function InsightCard({ title, detail, impact, confidence, tags = [], actionText, onAction, variant = 'standard', className = '' }) {
  const variantClasses = {
    standard: 'bg-slate-900/75 border-white/10',
    insight: 'bg-cyan-500/10 border-cyan-400/20',
    warning: 'bg-amber-500/10 border-amber-400/20',
    success: 'bg-emerald-500/10 border-emerald-400/20',
  }

  return (
    <article className={`rounded-3xl border p-5 shadow-[0_20px_50px_rgba(0,0,0,0.16)] ${variantClasses[variant]} ${className}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-300">{detail}</p>
        </div>
        <div className="text-right text-xs uppercase tracking-[0.2em] text-slate-400">{variant}</div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span key={tag} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">{tag}</span>
        ))}
      </div>
      <div className="mt-4 flex items-center justify-between gap-4 text-sm text-slate-400">
        {impact && <span>Impact: {impact}</span>}
        {confidence && <span>Confidence: {confidence}</span>}
      </div>
      {actionText && (
        <button onClick={onAction} className="mt-5 inline-flex rounded-full bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/15">
          {actionText}
        </button>
      )}
    </article>
  )
}

export default InsightCard
