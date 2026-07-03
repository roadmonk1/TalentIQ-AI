import Card from '../ui/Card'
import { useState } from 'react'

export function JobMatches({ jobs = [] }) {
  const [open, setOpen] = useState(null)

  return (
    <Card title={`Job matches — ${jobs.length} found`} className="col-span-2">
      <div className="space-y-3">
        {jobs.map((j) => (
          <div key={j.id} className="rounded-md border border-white/6 bg-slate-900/50 p-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-white">{j.title}</div>
                <div className="text-xs text-slate-400">{j.company}</div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-sm text-cyan-200">Match {j.score}%</div>
                <button onClick={() => setOpen(open === j.id ? null : j.id)} className="text-xs text-slate-300">{open === j.id ? 'Hide' : 'Why this match?'}</button>
              </div>
            </div>
            {open === j.id && (
              <div className="mt-3 text-sm text-slate-300">
                <div className="mb-2">Reason: {j.why}</div>
                <div className="text-xs text-slate-400">Missing skills: {j.missing_skills.join(', ')}</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  )
}

export default JobMatches
