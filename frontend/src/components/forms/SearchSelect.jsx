import { useId, useState } from 'react'
export default function SearchSelect({ label, options, value, onChange, multiple = false, disabled = false }) {
  const id = useId()
  const [query, setQuery] = useState('')
  const visible = options.filter((option) => option.label.toLowerCase().includes(query.toLowerCase()))
  return <fieldset disabled={disabled} className="rounded-lg border border-slate-300 p-3 dark:border-slate-600"><legend className="px-1 text-sm font-medium">{label}</legend><label className="text-xs text-slate-500" htmlFor={`${id}-search`}>Search {label.toLowerCase()}</label><input id={`${id}-search`} className="erp-input mt-1" value={query} onChange={(event) => setQuery(event.target.value)} />
    {multiple ? <div className="mt-3 max-h-44 space-y-2 overflow-auto">{visible.map((option) => <label key={option.value} className="flex items-start gap-3 text-sm"><input className="mt-1 accent-teal-700" type="checkbox" disabled={option.disabled} checked={value.includes(option.value)} onChange={(event) => onChange(event.target.checked ? [...value,option.value] : value.filter((entry) => entry !== option.value))} /><span>{option.label}{option.disabled && <span className="block text-xs text-slate-500">Restricted administrator control</span>}</span></label>)}{visible.length === 0 && <p className="text-sm text-slate-500">No matching options.</p>}</div> : <><label htmlFor={`${id}-select`} className="sr-only">Select {label}</label><select id={`${id}-select`} className="erp-input mt-2" value={value} onChange={(event) => onChange(event.target.value)}><option value="">Choose an option</option>{visible.map((option) => <option key={option.value} value={option.value} disabled={option.disabled}>{option.label}</option>)}</select></>}
  </fieldset>
}
