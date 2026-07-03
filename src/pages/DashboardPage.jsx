import { useMemo, useState, useEffect } from 'react'
import GreetingCard from '../components/dashboard/GreetingCard'
import ProfileCompletionCard from '../components/dashboard/ProfileCompletionCard'
import CareerScoreCard from '../components/dashboard/CareerScoreCard'
import ResumeScoreCard from '../components/dashboard/ResumeScoreCard'
import SkillGapCard from '../components/dashboard/SkillGapCard'
import AIMentorPanel from '../components/dashboard/AIMentorPanel'
import DailyMissionCard from '../components/dashboard/DailyMissionCard'
import WeeklyGoalsCard from '../components/dashboard/WeeklyGoalsCard'
import RecentActivity from '../components/dashboard/RecentActivity'
import UpcomingInterviews from '../components/dashboard/UpcomingInterviews'
import JobMatches from '../components/dashboard/JobMatches'
import CareerRoadmap from '../components/dashboard/CareerRoadmap'
import LearningRecommendations from '../components/dashboard/LearningRecommendations'
import AIInsights from '../components/dashboard/AIInsights'
import QuickActions from '../components/dashboard/QuickActions'
import AITimeline from '../components/dashboard/AITimeline'
import { getDashboard } from '../services/dashboardService'

export function DashboardPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    getDashboard()
      .then((res) => {
        if (!mounted) return
        setData(res.dashboard)
        setError(null)
      })
      .catch((err) => {
        if (!mounted) return
        setError(err.message || String(err))
      })
      .finally(() => mounted && setLoading(false))
    return () => {
      mounted = false
    }
  }, [])

  const handleAccept = (insight) => {
    // Create a mission from insight
    const mission = insight.text
    const newGoal = { id: Date.now(), title: insight.text, progress: 0 }

    setData((prev) => {
      const next = { ...prev }
      next.missions = { ...prev.missions }
      next.missions.today = mission
      next.missions.weeklyGoals = [newGoal, ...prev.missions.weeklyGoals]
      // remove accepted insight from ai.insights
      next.ai = { ...prev.ai }
      next.ai.insights = prev.ai.insights.filter((i) => i.id !== insight.id)
      // add timeline event
      next.timeline = [{ id: Date.now(), type: 'mission_created', text: `Mission added: ${insight.text}`, when: 'just now' }, ...(prev.timeline || [])]
      return next
    })
  }

  const handleCompleteMission = () => {
    setData((prev) => {
      const next = { ...prev }
      next.missions = { ...prev.missions }
      next.missions.today = 'No mission for today — check AI Mentor.'
      // mark weekly goal progress for the top goal
      if (next.missions.weeklyGoals && next.missions.weeklyGoals.length > 0) {
        next.missions.weeklyGoals[0] = { ...next.missions.weeklyGoals[0], progress: Math.min(1, next.missions.weeklyGoals[0].progress + 0.25) }
      }
      next.timeline = [{ id: Date.now(), type: 'mission_completed', text: 'Daily mission completed', when: 'just now' }, ...(prev.timeline || [])]
      return next
    })
  }

  const handleAddWeeklyGoal = (title) => {
    const newGoal = { id: Date.now(), title: title || 'New goal', progress: 0 }
    setData((prev) => ({ ...prev, missions: { ...prev.missions, weeklyGoals: [newGoal, ...(prev.missions.weeklyGoals || [])] }, timeline: [{ id: Date.now(), type: 'goal_added', text: `Weekly goal added: ${title}`, when: 'just now' }, ...(prev.timeline || [])] }))
  }

  if (loading) {
    return (
      <section className="mx-auto min-h-[60vh] max-w-7xl px-6 py-12 sm:px-8 lg:px-10">
        <div className="text-center text-slate-300">Loading dashboard…</div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="mx-auto min-h-[60vh] max-w-7xl px-6 py-12 sm:px-8 lg:px-10">
        <div className="text-center text-rose-400 mb-4">Failed to load dashboard: {error}</div>
        <div className="text-center">
          <button onClick={() => window.location.reload()} className="rounded-full bg-white/6 px-4 py-2">Retry</button>
        </div>
      </section>
    )
  }

  return (
    <section className="mx-auto min-h-[80vh] max-w-7xl px-6 py-12 sm:px-8 lg:px-10">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-8 space-y-6">
          <GreetingCard user={{ full_name: data.user.full_name, recommendations: data.ai.recommendations }} />

          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <CareerScoreCard score={data.scores.careerScore} breakdown={data.scores.breakdowns?.career} />
            <ResumeScoreCard score={data.scores.resumeScore} breakdown={data.scores.breakdowns?.resume} />
            <div>
              <ProfileCompletionCard completion={data.user.profile_completion} />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <AIMentorPanel insights={data.ai.insights} onAccept={handleAccept} />
            <SkillGapCard gaps={data.skillGaps} />
            <QuickActions />
          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <DailyMissionCard mission={data.missions.today} onComplete={handleCompleteMission} />
            <WeeklyGoalsCard goals={data.missions.weeklyGoals} onAddGoal={() => handleAddWeeklyGoal(data.missions.today)} />
            <RecentActivity activity={data.activity} />
          </div>
        </div>

        <aside className="lg:col-span-4 space-y-6">
          <UpcomingInterviews interviews={data.interviews} />
          <JobMatches jobs={data.jobs} />
          <CareerRoadmap />
          <LearningRecommendations />
          <AIInsights insights={data.ai.insights} />
          <AITimeline events={data.timeline} />
        </aside>
      </div>
    </section>
  )
}

export default DashboardPage
