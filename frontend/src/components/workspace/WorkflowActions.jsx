import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuth } from '../../auth/useAuth'
import { actions } from '../../workspaces/actions'
import { defaultsFor, schemaFor } from '../../forms/schemas'
import Modal from '../ui/Modal'
import Button from '../ui/Button'
import Field from '../forms/Field'
import AttachmentInput from '../forms/AttachmentInput'
function ActionForm({ action }) {
  const [reviewed,setReviewed] = useState(false)
  const form = useForm({ resolver: zodResolver(schemaFor(action.fields)), defaultValues: defaultsFor(action.fields) })
  return <form onSubmit={form.handleSubmit(() => setReviewed(true))} className="space-y-5"><p className="text-sm leading-6 text-slate-500">This action is not available yet. You can review its input requirements; no business record will change.</p><p className="text-xs text-slate-500">Eligible record states: {action.states.map((state) => state.replaceAll('_',' ')).join(', ')}. The server must confirm the record state and your permissions.</p><div className="grid gap-4 sm:grid-cols-2">{action.fields.map((field) => <Field key={field.name} field={field} register={form.register} error={form.formState.errors[field.name]} />)}</div>{action.label === 'Import statement' && <AttachmentInput />}{reviewed && <p role="status" className="rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-800">Input checked locally. This action has not been submitted.</p>}<div className="flex flex-wrap gap-3"><Button type="submit" variant="secondary">Review input</Button><Button disabled title="This action is not available yet">{action.label}</Button></div></form>
}
export default function WorkflowActions({ resource, record }) {
  const { can } = useAuth()
  const [selected,setSelected] = useState(null)
  const allowed = resource.actions.filter((key) => can(`${resource.module}:${actions[key].grant}`))
  if (!allowed.length) return null
  return <section className="erp-panel mt-6 p-5"><h2 className="font-semibold">Workflow actions</h2><p className="mt-2 text-sm text-slate-500">Review the requirements for each step. Actions remain unavailable until records can be processed.</p><div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">{allowed.map((key) => { const action=actions[key]; const stateAllowed = record && action.states.includes(record.status); return <div key={key} className="rounded-lg border border-slate-200 p-4 dark:border-slate-700"><p className="text-sm font-medium">{action.label}</p><p className="mt-1 text-xs text-slate-500">{record && !stateAllowed ? `Not applicable while ${record.status}.` : 'Currently unavailable.'}</p><button type="button" onClick={() => setSelected(key)} className="mt-3 text-sm font-medium text-teal-700 dark:text-teal-300">Review {action.label.toLowerCase()} requirements</button></div> })}</div><Modal open={!!selected} onClose={() => setSelected(null)} title={selected ? actions[selected].label : 'Action'} drawer>{selected && <ActionForm key={selected} action={actions[selected]} />}</Modal></section>
}
