import { Inbox, LockKeyhole, CircleAlert, Clock3, LoaderCircle } from 'lucide-react'
import Button from './Button'
export default function StatePanel({ state, title, children, onRetry, requestId }) {
  const Icon = { loading: LoaderCircle, empty: Inbox, denied: LockKeyhole, error: CircleAlert, unavailable: Clock3 }[state] || Inbox
  return <div className="rounded-xl border border-dashed border-slate-300 p-7 text-center dark:border-slate-700" role={state === 'error' ? 'alert' : 'status'}><Icon size={26} className={`mx-auto mb-3 text-slate-400 ${state === 'loading' ? 'animate-spin' : ''}`} /><h2 className="text-base font-semibold">{title || {loading:'Loading records…',empty:'No records yet',denied:'Access restricted',error:'Unable to load records',unavailable:'This workspace is not available yet'}[state]}</h2>{children && <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-500 dark:text-slate-400">{children}</p>}{requestId && <p className="mt-2 break-all text-xs text-slate-500">Support reference: {requestId}</p>}{onRetry && <Button variant="secondary" className="mt-4" onClick={onRetry}>Try again</Button>}</div>
}
