import Card from '../ui/Card'

export function WeeklyGoalsCard({ goals = [], onAddGoal }) {
  return (
    <Card title="Weekly goals">
      <div className="space-y-3">
        {goals.map((g) => (
          <div key={g.id} className="flex items-center justify-between">
            <div>
              <div className="text-sm text-white">{g.title}</div>
              <div className="text-xs text-slate-400">{Math.round(g.progress * 100)}% complete</div>
            </div>
            <div className="w-24">
              <div className="h-2 rounded-full bg-white/8">
                <div className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-violet-500" style={{ width: `${g.progress * 100}%` }} />
              </div>
            </div>
          </div>
        ))}
        {onAddGoal && (
          <div className="mt-2">
            <button onClick={onAddGoal} className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Add as weekly goal</button>
          </div>
        )}
      </div>
    </Card>
  )
}

export default WeeklyGoalsCard
