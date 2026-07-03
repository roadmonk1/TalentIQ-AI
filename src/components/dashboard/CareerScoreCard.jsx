import Card from '../ui/Card'
import DonutChart from '../ui/DonutChart'

export function CareerScoreCard({ score, breakdown = [] }) {
  return (
    <Card title="Career Score">
      <div className="flex items-center gap-4">
        <div className="w-24">
          <DonutChart value={score} />
        </div>
        <div className="flex-1">
          <div className="text-2xl font-semibold text-white">{score}%</div>
          <div className="mt-1 text-sm text-slate-400">Overall readiness across skills, roles, and visibility.</div>
          {breakdown && breakdown.length > 0 && (
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-300">
              {breakdown.map((b) => (
                <div key={b.label} className="flex items-center justify-between">
                  <div>{b.label}</div>
                  <div className="ml-2">{b.value}%</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}

export default CareerScoreCard
