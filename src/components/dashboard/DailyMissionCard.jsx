import Card from '../ui/Card'

export function DailyMissionCard({ mission, onComplete }) {
  return (
    <Card title="Daily mission">
      <div className="text-sm text-slate-200">{mission}</div>
      <div className="mt-3 flex items-center gap-2">
        <button onClick={onComplete} className="rounded-full bg-emerald-500/10 px-3 py-1 text-sm text-emerald-200">Mark done</button>
        <div className="text-xs text-slate-400">Complete this task for steady momentum.</div>
      </div>
    </Card>
  )
}

export default DailyMissionCard
