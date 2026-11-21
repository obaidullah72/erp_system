export default function Input({ label, id, error, ...props }) {
  return <div><label htmlFor={id} className="mb-1.5 block text-sm font-medium">{label}</label><input id={id} aria-invalid={!!error} aria-describedby={error ? `${id}-error` : undefined} className="w-full rounded-lg border border-slate-300 bg-transparent px-3 py-2.5 text-sm focus:outline-2 focus:outline-teal-600 dark:border-slate-600" {...props} />{error && <p id={`${id}-error`} className="mt-1 text-sm text-red-600">{error}</p>}</div>
}
