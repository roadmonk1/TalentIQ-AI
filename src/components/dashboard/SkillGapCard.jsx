import Card from '../ui/Card'

export function SkillGapCard({ gaps = [] }) {
  return (
    <Card title="Skill gaps">
      <div className="space-y-3">
        {gaps.map((g) => (
          <div key={g.skill} className="flex items-center justify-between">
            <div className="text-sm text-slate-300">{g.skill}</div>
            <div className="w-40">
              <div className="h-2 rounded-full bg-white/8">
                <div className="h-2 rounded-full bg-gradient-to-r from-rose-400 to-amber-400" style={{ width: `${g.gap}%` }} />
              </div>
            </div>
            <div className="ml-3 text-sm text-slate-400">{g.gap}% gap</div>
          </div>
        ))}
      </div>
    </Card>
  )
}

export default SkillGapCard
