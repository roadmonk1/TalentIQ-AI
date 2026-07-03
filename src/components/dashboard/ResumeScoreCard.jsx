import Card from '../ui/Card'
import DonutChart from '../ui/DonutChart'

export function ResumeScoreCard({ score, breakdown = [] }) {
  return (
    <Card title="Resume Score">
      <div className="flex items-center gap-4">
        <div className="w-20">
          <DonutChart value={score} />
        </div>
        <div className="flex-1">
          <div className="text-xl font-semibold text-white">{score}%</div>
          <div className="mt-1 text-sm text-slate-400">ATS and recruiter-friendly score with suggestions.</div>
          {breakdown && breakdown.length > 0 && (
            <div className="mt-3 text-xs text-slate-300">
              {breakdown.map((b) => (
                <div key={b.label} className="flex items-center justify-between">
                  <div>{b.label}</div>
                  <div>{b.value}%</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}

export default ResumeScoreCard
