import Card from '../ui/Card'
import DonutChart from '../ui/DonutChart'

export function ProfileCompletionCard({ completion }) {
  return (
    <Card title="Profile completion">
      <div className="flex items-center gap-4">
        <div className="w-20">
          <DonutChart value={completion} />
        </div>
        <div>
          <div className="text-lg font-semibold text-white">{completion}% complete</div>
          <div className="mt-1 text-sm text-slate-400">Complete your profile to improve recruiter matches.</div>
        </div>
      </div>
    </Card>
  )
}

export default ProfileCompletionCard
