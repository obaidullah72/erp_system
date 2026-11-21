export default function EmptyState({ title, children }) {
  return <div className="rounded-xl border border-dashed border-slate-300 p-8 dark:border-slate-700"><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">{children}</p></div>
}
