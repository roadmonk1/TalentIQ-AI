export function CoachMessage({ role = 'assistant', message, timestamp, reasoning, citations = [], status = 'normal', className = '' }) {
  const roleClasses = {
    assistant: 'bg-slate-900/70 border-cyan-400/10',
    user: 'bg-white/5 border-white/10',
    system: 'bg-slate-800/70 border-slate-600/40',
  }

  return (
    <div className={`rounded-[2rem] border p-5 ${roleClasses[role]} ${className}`}>
      <div className="flex items-center justify-between gap-3 text-sm font-semibold text-slate-200">
        <span>{role === 'assistant' ? 'TalentCoach' : role === 'user' ? 'You' : 'System'}</span>
        <span className="text-slate-400">{timestamp}</span>
      </div>
      <p className="mt-3 text-sm leading-7 text-slate-300">{message}</p>
      {reasoning && (
        <div className="mt-4 rounded-3xl bg-white/5 p-4 text-sm text-slate-300">
          <div className="font-semibold text-slate-100">Reasoning</div>
          <p className="mt-2 text-sm leading-6 text-slate-300">{reasoning}</p>
        </div>
      )}
      {citations.length > 0 && (
        <div className="mt-4 space-y-2 text-xs text-slate-400">
          <div className="font-semibold text-slate-100">Citations</div>
          {citations.map((citation, index) => (
            <div key={index} className="rounded-2xl bg-white/5 p-3">{citation}</div>
          ))}
        </div>
      )}
    </div>
  )
}

export default CoachMessage
