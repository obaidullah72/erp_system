const phases = [
  ['Foundation', 'Application shell, API, database connectivity, migrations, and containers.'],
  ['Master-data preparation', 'Foundation identity is implemented. Extend master data and organization settings next.'],
  ['Master data', 'Products, categories, brands, units, warehouses, and business partners.'],
  ['Inventory', 'Stock movements, reservations, transfers, returns, adjustments, and valuation.'],
  ['Purchasing, sales & POS', 'Receipts, invoices, payment capture, and posting integration.'],
  ['Accounting', 'Immutable journals, receivables, payables, cash, bank, expenses, and reconciliation.'],
  ['Manufacturing', 'BOMs, schedules, batches, quality, traceability, and production costing.'],
  ['Dashboard & reporting', 'Reports and visualizations backed by real business records.'],
  ['Hardening & deployment', 'Security, load tests, backups, restore drills, and release validation.'],
]
export default function RoadmapPage() {
  return <><p className="text-xs font-semibold uppercase tracking-widest text-teal-600">Implementation plan</p><h1 className="mt-2 text-3xl font-semibold">Nine phases. One foundation.</h1><p className="mt-3 text-sm text-slate-500">Phase 1 is the scope of this release. All remaining phases are planned.</p><ol className="mt-8 space-y-3">{phases.map(([title, description], index) => <li key={title} className="flex items-start gap-4 rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"><span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-sm font-semibold ${index === 0 ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-500 dark:bg-slate-800'}`}>{String(index + 1).padStart(2, '0')}</span><div><h2 className="text-sm font-semibold">{title}<span className="ml-3 text-xs font-normal text-slate-500">{index === 0 ? 'This release' : 'Planned'}</span></h2><p className="mt-2 text-xs leading-5 text-slate-500">{description}</p></div></li>)}</ol></>
}
