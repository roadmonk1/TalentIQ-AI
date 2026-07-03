import Card from '../ui/Card'

export function UpcomingInterviews({ interviews = [] }) {
  return (
    <Card title="Upcoming interviews">
      <div className="space-y-3">
        {interviews.map((i) => (
          <div key={i.id} className="flex items-center justify-between">
            <div>
              <div className="text-sm text-white">{i.company}</div>
              <div className="text-xs text-slate-400">{i.type} — {i.date}</div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

export default UpcomingInterviews
