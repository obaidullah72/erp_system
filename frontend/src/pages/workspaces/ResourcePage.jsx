import { useCallback, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { useListState } from '../../hooks/useListState'
import { useResource } from '../../hooks/useResource'
import { serviceFor } from '../../services/resources'
import { label } from '../../workspaces/catalog'
import PageHeading from '../../components/workspace/PageHeading'
import FilterBar from '../../components/workspace/FilterBar'
import DataTable from '../../components/tables/DataTable'
import StatePanel from '../../components/ui/StatePanel'
import Button from '../../components/ui/Button'
import Badge from '../../components/ui/Badge'
import MetricCard from '../../components/workspace/MetricCard'
import SpecializedView from '../../components/workspace/SpecializedView'
import WorkflowActions from '../../components/workspace/WorkflowActions'
import ExportPanel from '../../components/workspace/ExportPanel'
import PrintPreview from '../../components/workspace/PrintPreview'
export default function ResourcePage({resource}) {
  const {can,user}=useAuth();const location=useLocation();const {state,update}=useListState();const [print,setPrint]=useState(false)
  const connected=resource.status==='connected';const allowed=can(resource.readPermission)
  const params=JSON.stringify({page:state.page,page_size:state.page_size,q:state.q,active:state.active})
  const load=useCallback((signal)=>serviceFor(resource).list(JSON.parse(params),signal),[resource,params])
  const result=useResource(load,connected&&allowed)
  if(!allowed)return <StatePanel state="denied" title={`${resource.title} access required`}>Your current role does not allow this workspace. Ask an administrator to review your access.</StatePanel>
  const columns=connected?resource.id==='users'?['name','email','active','version']:['name','system','version']:resource.columns
  return <><PageHeading eyebrow={resource.group} title={resource.title} description={connected?'Manage confirmed business records. Changes are protected by server permissions and version checks.':'Review records, required inputs and workflow steps. This business capability is not available yet.'}><Badge>{connected?'Connected':'Unavailable'}</Badge>{resource.writable&&can(resource.createPermission)&&(resource.id!=='roles'||user.roles.includes('Super Admin'))&&<Link className="inline-flex items-center rounded-lg bg-teal-700 px-4 py-2.5 text-sm font-medium text-white" to={`${resource.path}/new${location.search}`}>{connected?'Create':'Prepare'} {resource.id==='users'?'user':resource.id==='roles'?'role':'draft'}</Link>}<Button variant="secondary" onClick={()=>setPrint(true)}>Print preview</Button></PageHeading>
  <FilterBar state={state} update={update} filters={resource.filters} connected={connected} roles={resource.id==='roles'}/>
  <SpecializedView resource={resource} state={state} update={update}/>
  {!!resource.metrics.length&&<div className="mb-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{resource.metrics.map((metric)=><MetricCard key={metric} label={label(metric)} note={metric.includes('quantity')||['planned','consumed','produced','accepted','rejected','remaining','on_hand','reserved','available'].includes(metric)?'Grouped by compatible units when records are available.':'Server-confirmed amounts only.'}/>)}</div>}
  {!connected&&<div className="mb-5"><StatePanel state="unavailable" title={`${resource.title} is not available yet`}>No production records or financial totals are shown. Your filters are preserved for this workspace.</StatePanel></div>}
  {connected&&result.status==='loading'?<StatePanel state="loading"/>:connected&&result.status==='error'?<StatePanel state={result.error.response?.status===403?'denied':'error'} onRetry={result.retry} requestId={result.error.requestId}>{result.error.userMessage||result.error.message}</StatePanel>:<DataTable columns={columns} rows={connected?result.data?.items||[]:[]} total={connected?result.data?.total:null} state={state} update={update} resourcePath={resource.path} sortable={!connected} caption={resource.title} unavailable={!connected}/>}
  {resource.kind==='report'&&<div className="mt-5 space-y-4"><p className="text-sm text-slate-500">Reporting period: {state.date_from||'Not selected'} to {state.date_to||'Not selected'}. Units and currency accompany each confirmed row; incompatible units are never combined.</p><ExportPanel canExport={can(`${resource.module}:export`)}/></div>}
  {!connected&&<WorkflowActions resource={resource}/>}
  <PrintPreview open={print} onClose={()=>setPrint(false)} title={resource.title} columns={columns}/></>
}
