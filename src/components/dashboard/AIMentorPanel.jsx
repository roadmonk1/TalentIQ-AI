import { useState } from 'react'
import { Link } from 'react-router-dom'
import MentorCard from '../mentor/MentorCard'

export function AIMentorPanel({ insights = [], onAccept }) {
  const [accepted, setAccepted] = useState([])

  const handleAccept = (insight) => {
    setAccepted((s) => [...s, insight.id])
    if (onAccept) onAccept(insight)
  }

  return (
    <MentorCard title="TalentCoach" subtitle="Daily career guidance from your AI mentor." variant="highlight" className="space-y-4">
      <div className="space-y-4">
        {insights.slice(0, 3).map((i) => (
          <div key={i.id} className="rounded-3xl border border-white/10 bg-slate-950/65 p-4">
            <div className="text-sm text-slate-200">{i.text}</div>
            <div className="mt-2 flex items-center justify-between gap-4 text-xs text-slate-400">
              <span>Impact +{i.impact}%</span>
              <div className="flex gap-2">
                <button disabled={accepted.includes(i.id)} onClick={() => handleAccept(i)} className="rounded-full bg-cyan-500/10 px-3 py-1 text-sm text-cyan-200 transition hover:bg-cyan-500/15 disabled:cursor-not-allowed disabled:opacity-50">
                  {accepted.includes(i.id) ? 'Accepted' : 'Accept'}
                </button>
                <button className="rounded-full bg-white/5 px-3 py-1 text-xs text-slate-300">Snooze</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Link to="/talentcoach" className="inline-flex items-center justify-center rounded-full bg-cyan-500/10 px-4 py-2 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-500/20">
          Open TalentCoach Workspace
        </Link>
        <span className="text-xs text-slate-500">Keep your career progress aligned and actionable.</span>
      </div>
    </MentorCard>
  )
}

export default AIMentorPanel
