import { useAuth } from '../auth/useAuth'
import EmptyState from '../components/ui/EmptyState'
export default function DashboardPage() {
  const { user } = useAuth()
  return <><p className="text-xs font-semibold uppercase tracking-widest text-teal-600">Workspace</p><h1 className="mt-2 text-3xl font-semibold">Welcome, {user.name}</h1><p className="mt-3 text-sm text-slate-500">{user.roles.join(' · ') || 'No roles assigned'}</p><div className="mt-8 grid gap-5 sm:grid-cols-2">{['Sales', 'Purchases', 'Inventory', 'Cash and bank'].map((name) => <EmptyState key={name} title={name}>Metrics are not available yet. This module’s transaction workflow is planned for a later stage.</EmptyState>)}</div><div className="mt-6 rounded-xl bg-teal-50 p-5 text-sm leading-6 text-teal-900 dark:bg-teal-950 dark:text-teal-200">Your identity, permissions, and business configuration are connected. The foundation includes an internal accounting posting service; operational modules and financial reports are not enabled.</div></>
}
