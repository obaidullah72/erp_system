import { AlertCircle } from 'lucide-react'

export default function ErrorState({ title = 'Something went wrong', message, requestId, onRetry }) {
  return <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-6 text-rose-900 dark:border-rose-900 dark:bg-rose-950 dark:text-rose-100"><AlertCircle className="mb-3" /><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm">{message}</p>{requestId && <p className="mt-2 break-all font-mono text-xs">Request: {requestId}</p>}{onRetry && <button onClick={onRetry} className="mt-4 rounded-lg border border-current px-4 py-2 text-sm">Try again</button>}</div>
}
