import { useState } from 'react'
import { useAuth } from '../../auth/useAuth'
import { Menu, Moon, Sun } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

export default function Header({ onMenu, open }) {
  const { theme, toggleTheme } = useTheme()
  const { logout } = useAuth()
  const [error, setError] = useState('')
  async function signOut() { try { await logout() } catch { setError('Sign-out failed. Please retry.') } }
  return <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-5 dark:border-slate-800 dark:bg-slate-900 sm:px-8">
    <div className="flex items-center gap-3"><button onClick={onMenu} aria-label="Toggle navigation" aria-expanded={open} aria-controls="app-sidebar" className="lg:hidden"><Menu size={22} /></button><span className="text-sm text-slate-500 dark:text-slate-400">Workspace <span className="mx-2 text-slate-300">/</span> <span className="font-medium text-slate-800 dark:text-slate-200">Workspace</span></span></div>
    <div className="flex items-center gap-4">{error && <span role="alert" className="text-xs text-red-600">{error}</span>}<button onClick={signOut} className="text-sm">Sign out</button><span className="hidden rounded-md border border-slate-200 px-2.5 py-1 text-xs text-slate-500 dark:border-slate-700 sm:block">v0.1.0</span><button aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`} title="Toggle theme" onClick={toggleTheme} className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800">{theme === 'dark' ? <Sun size={19} /> : <Moon size={19} />}</button></div>
  </header>
}
