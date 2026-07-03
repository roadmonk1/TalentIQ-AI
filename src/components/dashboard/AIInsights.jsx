import Card from '../ui/Card'

export function AIInsights({ insights = [] }) {
  return (
    <Card title="AI insights">
      <div className="space-y-2 text-sm text-slate-300">
        {insights.map((i) => (
          <div key={i.id} className="">{i.text}</div>
        ))}
      </div>
    </Card>
  )
}

export default AIInsights
