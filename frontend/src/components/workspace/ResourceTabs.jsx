export default function ResourceTabs({ tabs, active, onChange }) {
  return <nav aria-label="Record sections" className="mb-5 flex gap-1 overflow-x-auto border-b border-slate-200 dark:border-slate-700">{tabs.map((tab) => <button key={tab} type="button" aria-current={active === tab ? 'page' : undefined} onClick={() => onChange(tab)} className={`shrink-0 border-b-2 px-4 py-3 text-sm font-medium ${active === tab ? 'border-teal-600 text-teal-700 dark:text-teal-300' : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'}`}>{tab}</button>)}</nav>
}
