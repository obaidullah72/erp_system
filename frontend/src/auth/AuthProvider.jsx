import { useEffect, useState } from 'react'
import { api, onSessionChange, refreshSession, setSession } from '../lib/axios'
import { AuthContext } from './useAuth'

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    let active = true
    const unsubscribe = onSessionChange(setUser)
    refreshSession().catch(() => {}).finally(() => { if (active) setLoading(false) })
    return () => { active = false; unsubscribe() }
  }, [])
  async function login(values) {
    const { data } = await api.post('/auth/login', values)
    setSession(data)
  }
  async function logout() {
    // Keep the current session on network failure so the user can retry revocation.
    try { await api.post('/auth/logout') } catch (error) {
      if (error.response?.status !== 401) throw error
      try { await refreshSession(); await api.post('/auth/logout') } catch (retryError) {
        if (retryError.response?.status !== 401) throw retryError
      }
    }
    setSession(null)
  }
  return <AuthContext.Provider value={{ user, loading, login, logout, can: (permission) => !!user?.permissions.includes(permission) }}>{children}</AuthContext.Provider>
}
