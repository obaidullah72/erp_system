import { useId } from 'react'
export default function Field({ field, register, error, disabled = false, prefix = '' }) {
  const id = useId()
  const path = prefix + field.name
  const props = { id, disabled, 'aria-invalid': !!error, 'aria-describedby': `${id}-hint${error ? ` ${id}-error` : ''}`, ...register(path) }
  return <div className={field.type === 'textarea' ? 'sm:col-span-2' : ''}><label htmlFor={id} className="mb-1.5 block text-sm font-medium">{field.label}{field.required && <span aria-hidden="true" className="text-teal-700"> *</span>}</label>
    {field.type === 'textarea' ? <textarea {...props} rows={3} className="erp-input" /> : field.type === 'select' ? <select {...props} className="erp-input"><option value="">Choose an option</option>{field.options.map((option) => <option key={option} value={option}>{option.replaceAll('_',' ')}</option>)}</select> : <input {...props} className="erp-input" type={['email','password','date'].includes(field.type) ? field.type : 'text'} inputMode={field.type === 'decimal' ? 'decimal' : field.type === 'integer' ? 'numeric' : undefined} autoComplete={field.type === 'password' ? 'new-password' : undefined} />}
    <p id={`${id}-hint`} className="mt-1 text-xs leading-5 text-slate-500">{field.description || (field.type === 'decimal' ? `Up to ${field.precision || 6} decimal places. Server validation applies.` : field.type === 'reference' ? 'Record UUID. Selection becomes available with the corresponding workspace.' : '')}</p>{error && <p id={`${id}-error`} className="mt-1 text-sm text-red-600 dark:text-red-400">{error.message}</p>}</div>
}
