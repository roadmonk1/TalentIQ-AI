import Card from '../ui/Card'

export function AITimeline({ events = [] }) {
  return (
    <Card title={`AI timeline — ${events.length} events`}>
      <div className="space-y-3 text-sm text-slate-300">
        {events.map((e) => (
          <div key={e.id} className="flex items-start gap-3">
            <div className="mt-1 h-2 w-2 rounded-full bg-cyan-400" />
            <div>
              <div className="text-slate-200">{e.text}</div>
              <div className="text-xs text-slate-500">{e.when}</div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

export default AITimeline
