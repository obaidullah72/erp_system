import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from '../components/layout/Sidebar'
import Header from '../components/layout/Header'

export default function AppLayout() {
  const [open, setOpen] = useState(false)
  return <div className="min-h-screen"><a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:z-50 focus:bg-white focus:p-3 focus:text-slate-900">Skip to content</a><Sidebar open={open} onClose={() => setOpen(false)} /><div className="lg:pl-64"><Header onMenu={() => setOpen(!open)} open={open} /><main id="main-content" className="mx-auto max-w-7xl p-5 sm:p-8 lg:p-10"><Outlet /></main><footer className="mx-5 mt-6 flex flex-wrap justify-between gap-2 border-t border-slate-200 py-5 text-xs text-slate-500 dark:border-slate-800 sm:mx-8"><span>TradeCore / Platform foundation</span><span>ERP workspaces · Business services in development</span></footer></div></div>
}
