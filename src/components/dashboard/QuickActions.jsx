import Card from '../ui/Card'
import UploadResume from '../UploadResume'

export function QuickActions() {
  return (
    <Card title="Quick actions">
      <div className="flex flex-wrap gap-2">
        <UploadResume userId={'demo_user'} />
        <button className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Run ATS scan</button>
        <button className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Start mock interview</button>
      </div>
    </Card>
  )
}

export default QuickActions
