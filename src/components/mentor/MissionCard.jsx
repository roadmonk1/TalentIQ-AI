export function MissionCard({ title, description, status = 'not_started', timeEstimate, impact, onAction, actionText = 'Start', className = '' }) {
  const statusClasses = {
    not_started: 'border-white/10 bg-slate-900/70',
    in_progress: 'border-cyan-400/20 bg-slate-900/80',
    done: 'border-emerald-400/20 bg-emerald-500/10',
  }

  return (
    <article className={`rounded-[1.5rem] border p-5 shadow-[0_18px_50px_rgba(0,0,0,0.18)] ${statusClasses[status]} ${className}`}>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-base font-semibold text-white">{title}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-300">{description}</p>
        </div>
        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.16em] text-slate-300">{status.replace('_', ' ')}</span>
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-4 text-sm text-slate-400">
        {impact && <span>Impact: {impact}</span>}
        {timeEstimate && <span>Time: {timeEstimate}</span>}
      </div>
      {onAction && (
        <button onClick={onAction} className="mt-5 inline-flex rounded-full bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/15">
          {actionText}
        </button>
      )}
    </article>
  )
}

export default MissionCard
