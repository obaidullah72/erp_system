import { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

export default function LoginPage() {
  const { user, loading, login } = useAuth()
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()
  if (loading) return <p role="status">Checking your session…</p>
  if (user) return <Navigate to="/" replace />
  async function submit(event) {
    event.preventDefault()
    setError(''); setBusy(true)
    const values = Object.fromEntries(new FormData(event.currentTarget))
    try {
      await login(values)
      const target = location.state?.from
      navigate(target?.startsWith('/') && !target.startsWith('//') ? target : '/', { replace: true })
    } catch (failure) { setError(failure.userMessage || 'Sign-in failed.') }
    finally { setBusy(false) }
  }
  return <><h1 className="text-2xl font-semibold">Sign in to your workspace</h1><p className="mt-2 text-sm text-slate-500">Use the business code and account provided by your administrator.</p><form onSubmit={submit} className="mt-7 space-y-5"><Input id="business" name="business" label="Business code" autoComplete="organization" pattern="[a-z0-9-]+" maxLength={80} required /><Input id="email" name="email" label="Email" type="email" autoComplete="username" maxLength={254} required /><Input id="password" name="password" label="Password" type="password" autoComplete="current-password" maxLength={256} required />{error && <p role="alert" className="text-sm text-red-600">{error}</p>}<Button type="submit" disabled={busy} className="w-full">{busy ? 'Signing in…' : 'Sign in'}</Button></form></>
}
