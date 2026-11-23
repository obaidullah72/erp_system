import { useFieldArray } from 'react-hook-form'
import Field from './Field'
import Button from '../ui/Button'
import { defaultsFor } from '../../forms/schemas'
export default function LineEditor({ fields, control, register, errors, disabled }) {
  const rows = useFieldArray({ control, name: 'lines' })
  return <section className="space-y-4"><div className="flex items-center justify-between"><h2 className="font-semibold">Document lines</h2><Button variant="secondary" disabled={disabled || rows.fields.length >= 100} onClick={() => rows.append(defaultsFor(fields))}>Add line</Button></div><p className="text-sm text-slate-500">Quantities retain their units. Totals, eligible stock and valuation require server confirmation.</p>{rows.fields.map((row,index) => <fieldset key={row.id} className="rounded-xl border border-slate-200 p-4 dark:border-slate-700" disabled={disabled}><legend className="px-2 text-sm font-medium">Line {index+1}</legend><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{fields.map((field) => <Field key={field.name} field={field} register={register} prefix={`lines.${index}.`} error={errors.lines?.[index]?.[field.name]} />)}</div><Button variant="secondary" className="mt-3" onClick={() => rows.remove(index)}>Remove line {index+1}</Button></fieldset>)}{errors.lines?.root?.message || errors.lines?.message ? <p role="alert" className="text-sm text-red-600">{errors.lines.root?.message || errors.lines.message}</p> : null}</section>
}
