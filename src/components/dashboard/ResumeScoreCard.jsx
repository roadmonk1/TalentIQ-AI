import Card from '../ui/Card'
import DonutChart from '../ui/DonutChart'
import { Info } from 'lucide-react'

export function ResumeScoreCard({ score, breakdown = [] }) {
  const cardTitle = (
    <div className="flex items-center justify-between">
      <span>Resume Score</span>
      <div className="group relative">
        <Info className="h-4 w-4 text-slate-500 hover:text-cyan-300 cursor-help transition-colors" />
        <div className="absolute right-0 top-6 hidden w-60 rounded-2xl border border-white/10 bg-slate-950/95 p-3.5 text-xs text-slate-300 shadow-2xl group-hover:block z-20 leading-relaxed backdrop-blur-md">
          <p className="font-semibold text-white">How it is calculated:</p>
          <ul className="mt-1.5 list-disc list-inside space-y-1 text-[10px] text-slate-400">
            <li>Keyword density match: 20%</li>
            <li>Action-verb achievements: 20%</li>
            <li>Structural & section checks: 25%</li>
            <li>Functional contact URLs: 10%</li>
            <li>Flesch reading ease: 25%</li>
          </ul>
        </div>
      </div>
    </div>
  )

  return (
    <Card title={cardTitle}>
      <div className="flex items-center gap-4">
        <div className="w-24">
          <DonutChart value={score} />
        </div>
        <div className="flex-1">
          <div className="text-2xl font-semibold text-white">{score}%</div>
          <div className="mt-1 text-xs text-slate-400">ATS and recruiter-friendly score with suggestions.</div>
          {breakdown && breakdown.length > 0 && (
            <div className="mt-3 grid grid-cols-2 gap-2 text-[10px] text-slate-300">
              {breakdown.map((b) => (
                <div key={b.label} className="flex items-center justify-between">
                  <div className="truncate text-slate-400">{b.label}</div>
                  <div className="ml-2 font-medium text-cyan-300">{b.value}%</div>
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
