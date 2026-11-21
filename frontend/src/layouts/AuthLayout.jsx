import { Outlet } from 'react-router-dom'
import { useTheme } from '../hooks/useTheme'
export default function AuthLayout() {
  const { theme, toggleTheme } = useTheme()
  return <main className="flex min-h-screen items-center justify-center bg-slate-50 px-5 dark:bg-slate-950"><div className="w-full max-w-md"><div className="mb-8 flex items-center justify-between"><span className="text-xl font-semibold text-teal-700 dark:text-teal-300">TradeCore ERP</span><button className="text-sm" onClick={toggleTheme}>Use {theme === 'dark' ? 'light' : 'dark'} theme</button></div><div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900"><Outlet /></div><p className="mt-6 text-center text-xs text-slate-500">Stage 1 · Secure workspace foundation</p></div></main>
}
