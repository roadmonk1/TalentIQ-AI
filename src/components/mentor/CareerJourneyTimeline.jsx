import MentorCard from './MentorCard'

export function CareerJourneyTimeline({ events = [] }) {
  return (
    <MentorCard title="Career journey" subtitle="Track major milestones and your momentum." variant="muted" className="space-y-4">
      {events.length > 0 ? (
        <div className="space-y-5">
          {events.map((event) => (
            <div key={event.id} className="flex items-start gap-4">
              <div className="mt-1 h-3 w-3 rounded-full bg-cyan-400" />
              <div>
                <div className="text-sm font-semibold text-white">{event.title}</div>
                <div className="mt-1 text-sm text-slate-400">{event.description}</div>
                <div className="mt-2 text-xs uppercase tracking-[0.2em] text-slate-500">{event.when}</div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">No career journey events available yet. Interact with TalentCoach to build your timeline.</div>
      )}
    </MentorCard>
  )
}

export default CareerJourneyTimeline
