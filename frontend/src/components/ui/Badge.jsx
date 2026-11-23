export default function Badge({ children, status }) {
  const value = status || children
  const tone = ['posted','approved','completed','active','pass'].includes(value) ? 'bg-teal-50 text-teal-800 dark:bg-teal-950 dark:text-teal-200' : ['rejected','reversed','cancelled','fail','disabled'].includes(value) ? 'bg-rose-50 text-rose-800 dark:bg-rose-950 dark:text-rose-200' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
  return <span className={`inline-flex rounded-md px-2.5 py-1 text-xs font-medium ${tone}`}>{String(value ?? 'Unavailable').replaceAll('_',' ')}</span>
}
