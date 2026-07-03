import MentorCard from './MentorCard'

export function DailyBriefingCard({ items = [] }) {
  return (
    <MentorCard title="Daily briefing" subtitle="What TalentCoach recommends for today." className="space-y-4" variant="default">
      {items.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2">
          {items.map((item) => (
            <div key={item.id} className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
              <div className="text-sm font-semibold text-white">{item.label}</div>
              <p className="mt-2 text-sm leading-6 text-slate-300">{item.description}</p>
              {item.detail && <div className="mt-3 text-xs uppercase tracking-[0.16em] text-cyan-300">{item.detail}</div>}
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">TalentCoach has not generated a daily briefing yet. Ask a question to get your first plan.</div>
      )}
    </MentorCard>
  )
}

export default DailyBriefingCard
