import { useRef, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useForm, useWatch } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { userSchema, roleSchema, applyBackendErrors } from '../../forms/schemas'
import { useAuth } from '../../auth/useAuth'
import { useNotification } from '../../hooks/useNotification'
import { useUnsavedChanges } from '../../hooks/useUnsavedChanges'
import { serviceFor } from '../../services/resources'
import Field from '../../components/forms/Field'
import SearchSelect from '../../components/forms/SearchSelect'
import UnsavedDialog from '../../components/forms/UnsavedDialog'
import Button from '../../components/ui/Button'
import StatePanel from '../../components/ui/StatePanel'
import PermissionMatrix from './PermissionMatrix'

export default function AdminForm({ resource, record, roles = [], permissions = [] }) {
  const isUser = resource.id === 'users'
  const { user } = useAuth()
  const superAdmin = user.roles.includes('Super Admin')
  const protectedTarget = record && (isUser ? roles.some((role) => record.role_ids.includes(role.id) && ['Super Admin','Admin'].includes(role.name)) && !superAdmin : ['Super Admin','Admin'].includes(record.name))
  const restricted = protectedTarget || !isUser && !superAdmin
  const defaults = isUser ? { name:record?.name || '',email:record?.email || '',password:'',role_ids:record?.role_ids || [],active:record?.active ?? true } : {name:record?.name || '',permissions:record?.permissions || []}
  const form = useForm({resolver:zodResolver(isUser ? userSchema(!!record) : roleSchema),defaultValues:defaults})
  const selectedRoles = useWatch({control:form.control,name:'role_ids'}) || []
  const selectedPermissions = useWatch({control:form.control,name:'permissions'}) || []
  const blocker = useUnsavedChanges(form.formState.isDirty)
  const [failure,setFailure] = useState(null)
  const [saved,setSaved] = useState(null)
  const lock = useRef(false)
  const { notify } = useNotification()
  async function submit(values) {
    if (lock.current || restricted) return
    lock.current=true;setFailure(null)
    try {
      const payload = isUser ? record ? {version:record.version,name:values.name,active:values.active,role_ids:values.role_ids,...(values.password ? {password:values.password} : {})} : {name:values.name,email:values.email,password:values.password,role_ids:values.role_ids} : record ? {version:record.version,permissions:values.permissions} : values
      const service=serviceFor(resource)
      const result=record ? await service.update(record.id,payload) : await service.create(payload)
      form.reset(values);notify(`${isUser ? 'User' : 'Role'} saved.`);setSaved(result)
    } catch(error) { applyBackendErrors(error,form.setError);setFailure(error) }
    finally { lock.current=false }
  }
  if (saved) return <Navigate replace to={`${resource.path}/${saved.id}`} />
  return <><form onSubmit={(event) => form.handleSubmit(submit)(event)} className="erp-panel space-y-6 p-5 sm:p-7">{restricted && <StatePanel state="denied" title="Protected administrator controls">These administrator assignments or grants cannot be changed from this account.</StatePanel>}<fieldset disabled={restricted || form.formState.isSubmitting} className="space-y-5"><legend className="mb-5 font-semibold">{isUser ? 'User details' : 'Role details'}</legend><div className="grid gap-5 sm:grid-cols-2"><Field field={{name:'name',label:isUser ? 'Full name' : 'Role name',type:'text',required:true}} register={form.register} error={form.formState.errors.name} disabled={!isUser && !!record} />{isUser && <><Field field={{name:'email',label:'Email',type:'email',required:true}} register={form.register} error={form.formState.errors.email} disabled={!!record} /><Field field={{name:'password',label:record ? 'New password (optional)' : 'Password',type:'password',required:!record,description:'12–256 characters. Changing a password revokes existing sessions.'}} register={form.register} error={form.formState.errors.password} /></>}</div>{isUser ? <><SearchSelect label="Assigned roles" multiple options={roles.map((role) => ({value:role.id,label:role.name,disabled:!superAdmin && ['Super Admin','Admin'].includes(role.name)}))} value={selectedRoles} onChange={(value) => form.setValue('role_ids',value,{shouldDirty:true,shouldValidate:true})} />{record && <label className="flex items-center gap-3 text-sm"><input type="checkbox" {...form.register('active')} className="accent-teal-700" />Active user (disabling revokes sessions)</label>}</> : <PermissionMatrix codes={permissions} selected={selectedPermissions} onChange={(value) => form.setValue('permissions',value,{shouldDirty:true})} viewer={record?.name === 'Viewer'} />}</fieldset>{failure && <StatePanel state={failure.response?.status===403 ? 'denied' : 'error'} title={failure.response?.status===409 ? 'Update conflict' : 'Could not save'} requestId={failure.requestId}>{failure.userMessage || failure.message}{failure.response?.status===409 && ' Your input is preserved. Review the latest record before retrying.'}</StatePanel>}<Button type="submit" disabled={restricted || form.formState.isSubmitting}>{form.formState.isSubmitting ? 'Saving…' : 'Save changes'}</Button></form><UnsavedDialog blocker={blocker} /></>
}
