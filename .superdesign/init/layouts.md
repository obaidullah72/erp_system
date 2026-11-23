# Existing application layouts
## DashboardLayout
Source: `frontend/src/layouts/DashboardLayout.jsx`

```jsx
export { default } from './AppLayout'

```

## AppLayout
Source: `frontend/src/layouts/AppLayout.jsx`

```jsx
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from '../components/layout/Sidebar'
import Header from '../components/layout/Header'

export default function AppLayout() {
  const [open, setOpen] = useState(false)
  return <div className="min-h-screen"><a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:z-50 focus:bg-white focus:p-3 focus:text-slate-900">Skip to content</a><Sidebar open={open} onClose={() => setOpen(false)} /><div className="lg:pl-64"><Header onMenu={() => setOpen(!open)} open={open} /><main id="main-content" className="mx-auto max-w-7xl p-5 sm:p-8 lg:p-10"><Outlet /></main><footer className="mx-5 mt-6 flex flex-wrap justify-between gap-2 border-t border-slate-200 py-5 text-xs text-slate-500 dark:border-slate-800 sm:mx-8"><span>TradeCore / Platform foundation</span><span>Phase 1 of 9 · Business workflows are not enabled</span></footer></div></div>
}

```

## AuthLayout
Source: `frontend/src/layouts/AuthLayout.jsx`

```jsx
import { Outlet } from 'react-router-dom'
import { useTheme } from '../hooks/useTheme'
export default function AuthLayout() {
  const { theme, toggleTheme } = useTheme()
  return <main className="flex min-h-screen items-center justify-center bg-slate-50 px-5 dark:bg-slate-950"><div className="w-full max-w-md"><div className="mb-8 flex items-center justify-between"><span className="text-xl font-semibold text-teal-700 dark:text-teal-300">TradeCore ERP</span><button className="text-sm" onClick={toggleTheme}>Use {theme === 'dark' ? 'light' : 'dark'} theme</button></div><div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900"><Outlet /></div><p className="mt-6 text-center text-xs text-slate-500">Stage 1 · Secure workspace foundation</p></div></main>
}

```

## Header
Source: `frontend/src/components/layout/Header.jsx`

```jsx
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
    <div className="flex items-center gap-3"><button onClick={onMenu} aria-label="Toggle navigation" aria-expanded={open} aria-controls="app-sidebar" className="lg:hidden"><Menu size={22} /></button><span className="text-sm text-slate-500 dark:text-slate-400">TradeCore <span className="mx-2 text-slate-300">/</span> <span className="font-medium text-slate-800 dark:text-slate-200">Workspace</span></span></div>
    <div className="flex items-center gap-4">{error && <span role="alert" className="text-xs text-red-600">{error}</span>}<button onClick={signOut} className="text-sm">Sign out</button><span className="hidden rounded-md border border-slate-200 px-2.5 py-1 text-xs text-slate-500 dark:border-slate-700 sm:block">v0.1.0</span><button aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`} title="Toggle theme" onClick={toggleTheme} className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800">{theme === 'dark' ? <Sun size={19} /> : <Moon size={19} />}</button></div>
  </header>
}

```

## Sidebar
Source: `frontend/src/components/layout/Sidebar.jsx`

```jsx
import { NavLink } from 'react-router-dom'
import { Boxes, X, ShieldCheck } from 'lucide-react'
import { navigation } from '../../app/navigation'

export default function Sidebar({ open, onClose }) {
  return <>
    {open && <button className="fixed inset-0 z-30 bg-slate-950/50 lg:hidden" aria-label="Close navigation" onClick={onClose} />}
    <aside id="app-sidebar" aria-label="Main navigation" className={`${open ? 'flex' : 'hidden'} fixed inset-y-0 left-0 z-40 w-64 flex-col bg-[#122b32] text-slate-200 lg:flex`}>
      <div className="flex h-20 items-center gap-3 border-b border-white/10 px-6">
        <span className="rounded-xl bg-teal-400/15 p-2 text-teal-300"><Boxes size={24} /></span>
        <div><span className="text-xl font-semibold tracking-tight text-white">TradeCore</span><p className="text-[10px] uppercase tracking-[.22em] text-slate-400">ERP foundation</p></div>
        <button onClick={onClose} aria-label="Close navigation" className="ml-auto lg:hidden"><X size={20} /></button>
      </div>
      <div className="p-4"><p className="px-3 pb-3 pt-4 text-[10px] font-semibold uppercase tracking-[.2em] text-slate-400">Workspace</p>
        <nav className="space-y-1">{navigation.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} end={to === "/"} onClick={onClose} className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-3 text-sm ${isActive ? 'bg-teal-400/15 font-medium text-teal-200' : 'text-slate-300 hover:bg-white/5'}`}><Icon size={18} />{label}</NavLink>)}</nav>
      </div>
      <div className="mx-5 mt-auto mb-6 rounded-xl border border-white/10 p-4"><ShieldCheck size={20} className="mb-3 text-teal-300" /><p className="text-sm font-medium text-white">Phase 1 · Foundation</p><p className="mt-2 text-xs leading-5 text-slate-400">Business modules will be introduced in later phases.</p></div>
    </aside>
  </>
}

```