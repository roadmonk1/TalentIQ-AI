import Card from '../ui/Card'

export function LearningRecommendations({ jobs = [] }) {
  return (
    <Card title="Learning recommendations">
      <div className="space-y-2 text-sm text-slate-300">
        <div>Coursera: Advanced React Patterns — 4 weeks</div>
        <div>Pluralsight: System Design Fundamentals — 6 weeks</div>
        <div>Udemy: TypeScript Deep Dive — 3 weeks</div>
      </div>
    </Card>
  )
}

export default LearningRecommendations
