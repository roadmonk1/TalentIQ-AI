import { useState } from 'react'
import { MessageSquare, X, Star } from 'lucide-react'
import api from '../services/api'
import { useLocation } from 'react-router-dom'

export default function FeedbackButton() {
  const [open, setOpen] = useState(false)
  const [rating, setRating] = useState(5)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)
  const location = useLocation()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await api.post('/dashboard/feedback', {
        rating,
        message,
        page: location.pathname
      })
      setSuccess(true)
      setTimeout(() => {
        setOpen(false)
        setSuccess(false)
        setMessage('')
        setRating(5)
      }, 2000)
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to send feedback')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-950/90 px-4 py-3 font-semibold text-cyan-200 shadow-[0_10px_35px_rgba(6,182,212,0.2)] backdrop-blur-md transition hover:-translate-y-0.5 hover:border-cyan-400/60 hover:bg-cyan-900/50 hover:shadow-[0_10px_35px_rgba(6,182,212,0.35)]"
      >
        <MessageSquare className="h-4 w-4 text-cyan-400" />
        <span className="text-xs tracking-wider uppercase">Beta Feedback</span>
      </button>

      {/* Modal */}
      {open && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/70 p-4 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-3xl border border-white/10 bg-slate-900/95 p-6 shadow-2xl backdrop-blur-md">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <div>
                <h3 className="text-lg font-semibold text-white">Share your feedback</h3>
                <p className="text-xs text-slate-400 mt-1">Help us improve the TalentIQ Alpha preview</p>
              </div>
              <button onClick={() => setOpen(false)} className="rounded-full p-1 text-slate-400 hover:bg-white/10 hover:text-white">
                <X className="h-5 w-5" />
              </button>
            </div>

            {success ? (
              <div className="py-8 text-center text-cyan-400">
                <span className="text-4xl">🎉</span>
                <p className="mt-4 font-semibold text-white">Thank you!</p>
                <p className="text-sm text-slate-400 mt-1">Your feedback helps us make TalentIQ better.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="mt-4 space-y-4">
                {error && (
                  <div className="rounded-2xl border border-rose-500/20 bg-rose-500/10 p-3 text-xs text-rose-300">
                    {error}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400">How would you rate this page?</label>
                  <div className="mt-2 flex gap-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setRating(star)}
                        className="text-slate-400 hover:text-yellow-400 transition"
                      >
                        <Star className={`h-8 w-8 ${star <= rating ? 'fill-yellow-400 text-yellow-400' : 'text-slate-600'}`} />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400">What went well, or what could be improved?</label>
                  <textarea
                    required
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    rows={4}
                    className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-sm text-white outline-none ring-0 placeholder:text-slate-600"
                    placeholder="Describe any bugs, design issues, or feature ideas..."
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full rounded-full bg-cyan-500 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-50"
                >
                  {loading ? 'Sending...' : 'Submit Feedback'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  )
}
