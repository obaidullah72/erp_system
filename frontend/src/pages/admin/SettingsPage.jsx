import { useCallback, useRef, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuth } from '../../auth/useAuth'
import { useResource } from '../../hooks/useResource'
import { useNotification } from '../../hooks/useNotification'
import { useUnsavedChanges } from '../../hooks/useUnsavedChanges'
import { settingsService } from '../../services/resources'
import { applyBackendErrors, businessSettingsSchema } from '../../forms/schemas'
import Field from '../../components/forms/Field'
import UnsavedDialog from '../../components/forms/UnsavedDialog'
import PageHeading from '../../components/workspace/PageHeading'
import StatePanel from '../../components/ui/StatePanel'
import Button from '../../components/ui/Button'
function SettingsForm({record}) {
  const {can}=useAuth();const {notify}=useNotification()
  const [version,setVersion]=useState(record.version);const [error,setError]=useState(null);const lock=useRef(false)
  const form=useForm({resolver:zodResolver(businessSettingsSchema),defaultValues:{currency:record.currency,timezone:record.timezone}})
  const blocker=useUnsavedChanges(form.formState.isDirty)
  async function submit(values){if(lock.current)return;lock.current=true;setError(null);try{const saved=await settingsService.update({...values,version});setVersion(saved.version);form.reset({currency:saved.currency,timezone:saved.timezone});notify('Business settings saved.')}catch(failure){setError(failure);applyBackendErrors(failure,form.setError)}finally{lock.current=false}}
  return <><form onSubmit={(event) => form.handleSubmit(submit)(event)} className="erp-panel space-y-5 p-6"><fieldset disabled={!can('settings:update')||form.formState.isSubmitting} className="grid gap-5 sm:grid-cols-2"><legend className="mb-4 font-semibold">Business configuration</legend>{[{name:'currency',label:'Base currency',type:'text',required:true,description:'Three-letter code. Locked after the first journal posting.'},{name:'timezone',label:'Business timezone',type:'text',required:true,description:'IANA identifier, for example Asia/Karachi.'}].map((field)=><Field key={field.name} field={field} register={form.register} error={form.formState.errors[field.name]}/>)}</fieldset><p className="text-xs text-slate-500">Version {version}</p>{error&&<StatePanel state={error.response?.status===403?'denied':'error'} title={error.response?.status===409?'Settings conflict':'Could not save settings'} requestId={error.requestId}>{error.userMessage||error.message} Your input has been preserved.</StatePanel>}<Button type="submit" disabled={!can('settings:update')||form.formState.isSubmitting}>{form.formState.isSubmitting?'Saving…':'Save settings'}</Button></form><section className="erp-panel mt-5 p-5"><h2 className="font-semibold">Accounting & stock policies</h2><p className="mt-2 text-sm text-slate-500">Fiscal year, tax rates, valuation and negative-stock policy configuration are not available yet. No production policy has been assumed.</p></section><UnsavedDialog blocker={blocker}/></>
}
export default function SettingsPage(){const {can}=useAuth();const load=useCallback((signal)=>settingsService.get(signal),[]);const result=useResource(load,can('settings:read'));if(!can('settings:read'))return <StatePanel state="denied"/>;return <><PageHeading title="Business settings" eyebrow="Administration" description="Manage the configuration confirmed by your business."/>{result.status==='loading'?<StatePanel state="loading"/>:result.status==='error'?<StatePanel state="error" onRetry={result.retry}>{result.error.userMessage||result.error.message}</StatePanel>:<SettingsForm record={result.data}/>}</>}
