import { Link } from 'react-router-dom'
export default function MetricCard({ label, value = null, unit, currency, href, note }) {
  return <article className="erp-panel p-5"><p className="text-sm text-slate-500 dark:text-slate-400">{label}</p><p className="mt-4 text-2xl font-semibold tabular-nums">{value == null ? <span className="text-slate-400">Unavailable</span> : <>{String(value)} <span className="text-sm">{currency || unit}</span></>}</p><p className="mt-2 text-xs leading-5 text-slate-500">{note || 'Awaiting confirmed transactions.'}</p>{href && <Link className="mt-4 inline-block text-sm font-medium text-teal-700 dark:text-teal-300" to={href}>View supporting records</Link>}</article>
}
