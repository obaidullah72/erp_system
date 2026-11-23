# Existing custom React primitives
## Input
Source: `frontend/src/components/ui/Input.jsx`

```jsx
export default function Input({ label, id, error, ...props }) {
  return <div><label htmlFor={id} className="mb-1.5 block text-sm font-medium">{label}</label><input id={id} aria-invalid={!!error} aria-describedby={error ? `${id}-error` : undefined} className="w-full rounded-lg border border-slate-300 bg-transparent px-3 py-2.5 text-sm focus:outline-2 focus:outline-teal-600 dark:border-slate-600" {...props} />{error && <p id={`${id}-error`} className="mt-1 text-sm text-red-600">{error}</p>}</div>
}

```

## EmptyState
Source: `frontend/src/components/ui/EmptyState.jsx`

```jsx
export default function EmptyState({ title, children }) {
  return <div className="rounded-xl border border-dashed border-slate-300 p-8 dark:border-slate-700"><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">{children}</p></div>
}

```

## Button
Source: `frontend/src/components/ui/Button.jsx`

```jsx
export default function Button({ children, className = '', ...props }) {
  return <button className={`rounded-lg bg-teal-700 px-4 py-2.5 text-sm font-medium text-white hover:bg-teal-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-600 disabled:cursor-not-allowed disabled:opacity-50 ${className}`} {...props}>{children}</button>
}

```

## ErrorState
Source: `frontend/src/components/ui/ErrorState.jsx`

```jsx
import { AlertCircle } from 'lucide-react'

export default function ErrorState({ title = 'Something went wrong', message, requestId, onRetry }) {
  return <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-6 text-rose-900 dark:border-rose-900 dark:bg-rose-950 dark:text-rose-100"><AlertCircle className="mb-3" /><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm">{message}</p>{requestId && <p className="mt-2 break-all font-mono text-xs">Request: {requestId}</p>}{onRetry && <button onClick={onRetry} className="mt-4 rounded-lg border border-current px-4 py-2 text-sm">Try again</button>}</div>
}

```