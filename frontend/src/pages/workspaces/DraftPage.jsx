import { useState } from 'react'
import { useForm, useWatch } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useLocation, useParams } from 'react-router-dom'
import { schemaFor, defaultsFor } from '../../forms/schemas'
import { useAuth } from '../../auth/useAuth'
import { useUnsavedChanges } from '../../hooks/useUnsavedChanges'
import Field from '../../components/forms/Field'
import LineEditor from '../../components/forms/LineEditor'
import AttachmentInput from '../../components/forms/AttachmentInput'
import UnsavedDialog from '../../components/forms/UnsavedDialog'
import StatePanel from '../../components/ui/StatePanel'
import Button from '../../components/ui/Button'
import PageHeading from '../../components/workspace/PageHeading'
import BarcodePreview from '../../components/workspace/BarcodePreview'
import PrintPreview from '../../components/workspace/PrintPreview'

export default function DraftPage({ resource }) {
  const { can } = useAuth()
  const { id } = useParams()
  const location = useLocation()
  const editing = !!id
  const [review,setReview] = useState(null)
  const [print,setPrint] = useState(false)
  const form = useForm({ resolver:zodResolver(schemaFor(resource.fields,resource.lines)), defaultValues:{...defaultsFor(resource.fields), ...(resource.lines ? {lines:[defaultsFor(resource.lines)]} : {})} })
  const barcodeValue = useWatch({control:form.control,name:'barcode'}) || ''
  const blocker = useUnsavedChanges(form.formState.isDirty)
  if (!can(editing ? resource.updatePermission : resource.createPermission)) return <StatePanel state="denied">You do not have permission to prepare this record.</StatePanel>
  return <><PageHeading eyebrow={resource.group} title={`${editing ? 'Edit' : 'Prepare'} ${resource.title.toLowerCase()}`} back={resource.path+location.search} description={editing ? `Record ${id}. Existing values cannot be loaded yet.` : 'Prepare and check input locally. Saving is unavailable; nothing is posted or added to the business.'} /><StatePanel state="unavailable" title={editing ? 'Existing record unavailable' : 'Saving is not available yet'}>{editing ? 'Editing requires the current record and version. Fields remain disabled until those are available.' : 'You can review required fields below. Keep a local printout if needed; this draft is not saved.'}</StatePanel><form className="erp-panel mt-6 space-y-6 p-5 sm:p-7" onSubmit={form.handleSubmit((values) => setReview(values))}><fieldset disabled={editing} className="grid gap-5 sm:grid-cols-2"><legend className="mb-5 font-semibold">Record details</legend>{resource.fields.map((field) => <Field key={field.name} field={field} register={form.register} error={form.formState.errors[field.name]} />)}</fieldset>{resource.lines && <LineEditor fields={resource.lines} control={form.control} register={form.register} errors={form.formState.errors} disabled={editing} />}{!editing && <AttachmentInput />}{review && <p role="status" className="rounded-lg bg-slate-100 p-4 text-sm dark:bg-slate-800">Input checked locally. No record has been saved, posted or valued.</p>}<div className="flex flex-wrap gap-3"><Button type="submit" variant="secondary" disabled={editing || form.formState.isSubmitting}>Review input</Button><Button disabled title="Saving is not available yet">Save draft</Button><Button variant="secondary" disabled={!review} onClick={() => setPrint(true)}>Print preview</Button></div></form>{resource.id === 'products' && <div className="mt-5"><BarcodePreview value={barcodeValue}/></div>}<PrintPreview open={print} onClose={() => setPrint(false)} title={resource.title} values={review} localDraft /><UnsavedDialog blocker={blocker} /></>
}
