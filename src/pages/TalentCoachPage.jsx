import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import mentorService from '../services/mentorService'
import MentorCard from '../components/mentor/MentorCard'
import { InsightCard } from '../components/mentor/InsightCard'
import { MissionCard } from '../components/mentor/MissionCard'
import { CoachMessage } from '../components/mentor/CoachMessage'
import { DailyBriefingCard } from '../components/mentor/DailyBriefingCard'
import { CareerJourneyTimeline } from '../components/mentor/CareerJourneyTimeline'
import { Skeleton } from '../components/ui/Skeleton'

const SESSION_STORAGE_KEY = 'talentcoach_session_id'

function generateSessionId() {
  if (window.crypto?.randomUUID) return window.crypto.randomUUID()
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

export function TalentCoachPage() {
  const { user, api } = useAuth()
  const [sessionId, setSessionId] = useState(() => localStorage.getItem(SESSION_STORAGE_KEY) || generateSessionId())
  const [sessionData, setSessionData] = useState(null)
  const [contextData, setContextData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [inputValue, setInputValue] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState(null)

  useEffect(() => {
    localStorage.setItem(SESSION_STORAGE_KEY, sessionId)
  }, [sessionId])

  useEffect(() => {
    if (!user || !api) return

    let mounted = true
    const loadMentor = async () => {
      setLoading(true)
      setError(null)

      try {
        const [sessionResponse, contextResponse] = await Promise.all([
          mentorService.getMentorSession(api, sessionId),
          mentorService.getMentorContext(api, sessionId, user.id),
        ])

        if (!mounted) return
        if (contextResponse?.session_id && contextResponse.session_id !== sessionId) {
          setSessionId(contextResponse.session_id)
        }

        setSessionData(sessionResponse)
        setContextData(contextResponse?.context || {})
      } catch (err) {
        if (!mounted) return
        setError(err.response?.data?.error || err.message || 'Unable to load TalentCoach session.')
      } finally {
        if (mounted) setLoading(false)
      }
    }

    loadMentor()
    return () => {
      mounted = false
    }
  }, [user, api, sessionId])

  const sessionSummary = sessionData?.summary || {}
  const weeklyGoals = contextData?.weekly_goals || []
  const timelineEvents = contextData?.mission_history || []
  const followUpQuestions = sessionSummary.follow_up_questions || []
  const conversationHistory = sessionData?.messages || []

  const dailyBriefing = useMemo(() => {
    if (Array.isArray(sessionSummary.daily_missions) && sessionSummary.daily_missions.length > 0) {
      return sessionSummary.daily_missions.map((mission, index) => ({
        id: mission.id || `daily-${index}`,
        label: mission.title || mission.name || `Mission ${index + 1}`,
        description: mission.description || mission.text || 'TalentCoach recommended this mission for your progress.',
        detail: mission.detail || mission.status || '',
      }))
    }

    return weeklyGoals.slice(0, 2).map((goal) => ({
      id: goal.id || goal.title,
      label: goal.title || 'Weekly goal',
      description: `Progress ${Math.round((goal.progress || 0) * 100)}%`,
      detail: 'Weekly planning',
    }))
  }, [sessionSummary.daily_missions, weeklyGoals])

  const careerInsights = useMemo(() => {
    const insights = []
    if (sessionSummary.next_best_action) {
      insights.push({
        id: 'best-action',
        title: 'Next best action',
        detail: sessionSummary.next_best_action,
        impact: sessionSummary.confidence ? `${Math.round(sessionSummary.confidence * 100)}%` : '',
        confidence: sessionSummary.confidence ? `${Math.round(sessionSummary.confidence * 100)}%` : 'N/A',
        tags: ['Action', 'Coach'],
      })
    }

    const firstGap = contextData?.skill_gaps?.[0]
    if (firstGap) {
      const gapText = typeof firstGap === 'string' ? firstGap : `${firstGap.skill || firstGap.label || 'Skill gap'} — ${firstGap.gap ?? firstGap.value ?? ''}%`
      insights.push({
        id: 'skill-gap',
        title: 'Top skill gap',
        detail: gapText,
        impact: 'Target this skill next',
        confidence: 'Coach recommended',
        tags: ['Skills'],
      })
    }

    if (contextData?.resume_health?.value) {
      insights.push({
        id: 'resume-health',
        title: 'Resume health',
        detail: `Score ${contextData.resume_health.value} out of 100`,
        impact: 'Resume',
        confidence: 'Live snapshot',
        tags: ['Resume'],
      })
    }

    return insights
  }, [contextData, sessionSummary])

  const weeklyPlanItems = useMemo(() => {
    if (Array.isArray(sessionSummary.weekly_plan) && sessionSummary.weekly_plan.length > 0) {
      return sessionSummary.weekly_plan.map((item, index) => ({
        id: item.id || `weekly-${index}`,
        title: item.title || item.name || `Plan item ${index + 1}`,
        description: item.description || item.summary || 'Weekly action item created by TalentCoach.',
        status: item.status || 'not_started',
        timeEstimate: item.time_estimate || item.estimate || '',
        impact: item.impact || '',
      }))
    }

    return []
  }, [sessionSummary.weekly_plan])

  const handleChatSubmit = async (message) => {
    if (!message?.trim()) {
      setChatError('Type a question for TalentCoach.')
      return
    }

    setChatLoading(true)
    setChatError(null)

    try {
      await mentorService.postMentorChat(api, {
        session_id: sessionId,
        user_id: user.id,
        message,
        target_career: 'default',
      })

      const [sessionResponse, contextResponse] = await Promise.all([
        mentorService.getMentorSession(api, sessionId),
        mentorService.getMentorContext(api, sessionId, user.id),
      ])

      setSessionData(sessionResponse)
      setContextData(contextResponse?.context || {})
      setInputValue('')
    } catch (err) {
      setChatError(err.response?.data?.error || err.message || 'Unable to send chat.')
    } finally {
      setChatLoading(false)
    }
  }

  const handleFollowUpClick = (question) => {
    handleChatSubmit(question)
  }

  if (loading) {
    return (
      <section className="mx-auto max-w-7xl px-6 py-12 sm:px-8 lg:px-10">
        <div className="space-y-6">
          <Skeleton className="h-6 w-48" />
          <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
            <div className="space-y-6">
              <Skeleton className="h-80" />
              <Skeleton className="h-80" />
            </div>
            <div className="space-y-6">
              <Skeleton className="h-96" />
            </div>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-7xl px-6 py-12 sm:px-8 lg:px-10">
      <div className="mb-8 flex flex-col gap-6 rounded-[2rem] border border-white/10 bg-slate-950/75 p-6 shadow-[0_20px_70px_rgba(0,0,0,0.3)] sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">TalentCoach Workspace</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-[-0.04em] text-white sm:text-5xl">Your career mentor, daily briefing, and growth timeline.</h1>
          <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">Stay focused on what moves your career forward with targeted guidance, action plans, and coach-approved milestones.</p>
        </div>
        <Link to="/dashboard" className="inline-flex items-center justify-center rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm font-semibold text-white transition hover:border-cyan-400/40 hover:bg-white/10">
          Back to dashboard
        </Link>
      </div>

      {error && (
        <div className="mb-6 rounded-3xl border border-rose-500/20 bg-rose-500/10 p-5 text-sm text-rose-100">
          {error}
        </div>
      )}

      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <div className="space-y-6">
          <MentorCard title="Ask TalentCoach" subtitle="Send a question and let the mentor update your session." variant="highlight" className="space-y-4">
            <div className="space-y-4">
              <textarea
                value={inputValue}
                onChange={(event) => setInputValue(event.target.value)}
                rows={4}
                className="w-full rounded-3xl border border-white/10 bg-slate-950/80 p-4 text-sm text-white outline-none ring-0 placeholder:text-slate-500"
                placeholder="Ask TalentCoach about your resume, interview prep, or next role."
              />
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <button
                  disabled={chatLoading}
                  onClick={() => handleChatSubmit(inputValue)}
                  className="inline-flex items-center justify-center rounded-full bg-cyan-500/10 px-5 py-3 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {chatLoading ? 'Sending…' : 'Send to TalentCoach'}
                </button>
                {chatError && <span className="text-sm text-rose-300">{chatError}</span>}
              </div>
            </div>
          </MentorCard>

          <DailyBriefingCard items={dailyBriefing} />

          <MentorCard title="Career insights" subtitle="Insights derived from your Mentor context." variant="default" className="space-y-5">
            <div className="grid gap-4 lg:grid-cols-2">
              {careerInsights.length > 0 ? (
                careerInsights.map((insight) => (
                  <InsightCard
                    key={insight.id}
                    title={insight.title}
                    detail={insight.detail}
                    impact={insight.impact}
                    confidence={insight.confidence}
                    tags={insight.tags}
                    actionText="Review"
                  />
                ))
              ) : (
                <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">TalentCoach has not produced career insights yet. Ask a question or refresh the page.</div>
              )}
            </div>
          </MentorCard>

          <MentorCard title="Mission board" subtitle="Your current missions and weekly plan." variant="highlight" className="space-y-5">
            {weeklyPlanItems.length > 0 ? (
              <div className="space-y-4">
                {weeklyPlanItems.map((item) => (
                  <MissionCard
                    key={item.id}
                    title={item.title}
                    description={item.description}
                    status={item.status}
                    timeEstimate={item.timeEstimate}
                    impact={item.impact}
                  />
                ))}
              </div>
            ) : (
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">No weekly plan items are available yet. Ask TalentCoach to create a plan.</div>
            )}
          </MentorCard>

          <MentorCard title="Follow-up questions" subtitle="Continue the conversation with TalentCoach." variant="default" className="space-y-4">
            {followUpQuestions.length > 0 ? (
              <div className="space-y-3">
                {followUpQuestions.map((question, index) => (
                  <button
                    key={`${question}-${index}`}
                    onClick={() => handleFollowUpClick(question)}
                    className="w-full rounded-3xl border border-white/10 bg-slate-950/70 px-4 py-3 text-left text-sm text-slate-200 transition hover:border-cyan-400/30 hover:bg-slate-900"
                  >
                    {question}
                  </button>
                ))}
              </div>
            ) : (
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">TalentCoach has not suggested follow-up questions yet.</div>
            )}
          </MentorCard>

          <MentorCard title="Conversation history" subtitle="Recent messages from your Mentor session." variant="muted" className="space-y-4">
            {conversationHistory.length > 0 ? (
              <div className="space-y-4">
                {conversationHistory.map((message, index) => (
                  <CoachMessage key={`${message.timestamp}-${index}`} role={message.role} message={message.text} timestamp={new Date(message.timestamp).toLocaleString()} citations={message.metadata?.citations || []} />
                ))}
              </div>
            ) : (
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-6 text-sm text-slate-400">No conversation history available yet. Send your first question to TalentCoach.</div>
            )}
          </MentorCard>
        </div>

        <aside className="space-y-6">
          <CareerJourneyTimeline events={timelineEvents} />

          <MentorCard title="Snapshot" subtitle="Quick, coach-approved health checks." variant="muted" className="space-y-4">
            <div className="grid gap-3">
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
                <div className="text-sm font-semibold text-white">Resume health</div>
                <div className="mt-2 text-sm text-slate-300">{contextData?.resume_health?.value ? `${contextData.resume_health.value}/100` : 'No live resume health data yet.'}</div>
              </div>
              <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-4">
                <div className="text-sm font-semibold text-white">Interview readiness</div>
                <div className="mt-2 text-sm text-slate-300">{contextData?.interview_memory?.history?.length ? `${contextData.interview_memory.history.length} sessions recorded` : 'No interview readiness data available yet.'}</div>
              </div>
            </div>
          </MentorCard>
        </aside>
      </div>
    </section>
  )
}

export default TalentCoachPage
