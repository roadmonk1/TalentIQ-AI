import Card from '../ui/Card'
import UploadResume from '../UploadResume'
import { useAuth } from '../../contexts/AuthContext'

export function QuickActions() {
  const { user } = useAuth()
  return (
    <Card title="Quick actions">
      <div className="flex flex-wrap gap-2">
        <UploadResume userId={user?.id} />
        <button className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Run ATS scan</button>
        <button className="rounded-full bg-white/6 px-3 py-2 text-sm text-white">Start mock interview</button>
      </div>
    </Card>
  )
}

export default QuickActions
