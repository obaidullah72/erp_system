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
