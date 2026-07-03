import Card from '../ui/Card'

export function RecentActivity({ activity = [] }) {
  return (
    <Card title="Recent activity">
      <div className="space-y-3">
        {activity.map((a) => (
          <div key={a.id} className="flex items-center justify-between text-sm">
            <div className="text-slate-300">{a.text}</div>
            <div className="text-xs text-slate-500">{a.time}</div>
          </div>
        ))}
      </div>
    </Card>
  )
}

export default RecentActivity
