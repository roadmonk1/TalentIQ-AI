import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, ShieldCheck, Sparkles } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export function AuthPage() {
  const { login, register } = useAuth()
  const [isSignUp, setIsSignUp] = useState(true)
  const [form, setForm] = useState({ full_name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    if (!form.email || !form.password || (isSignUp && !form.full_name)) {
      setError('Please complete all required fields.')
      setLoading(false)
      return
    }

    if (form.password.length < 8) {
      setError('Password must be at least 8 characters long.')
      setLoading(false)
      return
    }

    try {
      if (isSignUp) {
        await register({ full_name: form.full_name, email: form.email, password: form.password, role: 'Student' })
        setSuccess('Account created. You can sign in now.')
        setIsSignUp(false)
        setForm((current) => ({ ...current, full_name: '' }))
      } else {
        await login({ email: form.email, password: form.password })
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="mx-auto flex min-h-[80vh] max-w-6xl items-center justify-center px-6 py-16 sm:px-8 lg:px-10">
      <div className="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950/70 shadow-[0_0_80px_rgba(99,102,241,0.14)] lg:grid-cols-[0.95fr_1.05fr]">
        <div className="border-b border-white/10 bg-gradient-to-br from-cyan-500/15 via-slate-900/80 to-violet-500/15 p-8 lg:border-b-0 lg:border-r">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200">
            <Sparkles className="h-4 w-4" />
            Secure career intelligence
          </div>
          <h1 className="mt-6 text-3xl font-semibold text-white sm:text-4xl">Enter the TalentIQ network.</h1>
          <p className="mt-4 max-w-md text-base leading-8 text-slate-400">Create your account to unlock career analysis, interview prep, and recruiter-facing positioning tools.</p>
          <div className="mt-8 space-y-3 text-sm text-slate-300">
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3"><ShieldCheck className="h-4 w-4 text-cyan-200" />Encrypted account access and role-based permissions</div>
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3"><ShieldCheck className="h-4 w-4 text-cyan-200" />Multi-step onboarding for students, professionals, and recruiters</div>
          </div>
        </div>

        <div className="p-8 sm:p-10">
          <div className="flex rounded-full border border-white/10 bg-white/5 p-1">
            <button type="button" onClick={() => setIsSignUp(true)} className={`flex-1 rounded-full px-4 py-2 text-sm font-medium transition ${isSignUp ? 'bg-white text-slate-950' : 'text-slate-300'}`}>Sign up</button>
            <button type="button" onClick={() => setIsSignUp(false)} className={`flex-1 rounded-full px-4 py-2 text-sm font-medium transition ${!isSignUp ? 'bg-white text-slate-950' : 'text-slate-300'}`}>Sign in</button>
          </div>

          <h2 className="mt-8 text-2xl font-semibold text-white">{isSignUp ? 'Create your workspace' : 'Welcome back'}</h2>
          <p className="mt-2 text-sm text-slate-400">{isSignUp ? 'Simple, secure, and ready for future expansion.' : 'Continue where you left off.'}</p>

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            {isSignUp && (
              <div>
                <label className="mb-2 block text-sm text-slate-300" htmlFor="full_name">Full name</label>
                <input id="full_name" value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} className="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0" placeholder="Alex Morgan" />
              </div>
            )}
            <div>
              <label className="mb-2 block text-sm text-slate-300" htmlFor="email">Work email</label>
              <input id="email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} className="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0" placeholder="you@company.com" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300" htmlFor="password">Password</label>
              <input id="password" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} className="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0" placeholder={isSignUp ? 'Create a password' : 'Enter your password'} />
            </div>
            {error && <p className="rounded-2xl border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">{error}</p>}
            {success && <p className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-200">{success}</p>}
            <button type="submit" disabled={loading} className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-white px-5 py-3 font-medium text-slate-950 transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-70">
              {loading ? 'Please wait...' : isSignUp ? 'Create account' : 'Sign in'}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          <p className="mt-6 text-sm text-slate-400">Already have an account? <Link to="/" className="font-medium text-cyan-200 transition hover:text-cyan-100">Return home</Link></p>
        </div>
      </div>
    </section>
  )
}
