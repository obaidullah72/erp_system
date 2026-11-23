import { useCallback } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { useResource } from '../../hooks/useResource'
import { useListState } from '../../hooks/useListState'
import { serviceFor } from '../../services/resources'
import { label } from '../../workspaces/catalog'
import PageHeading from '../../components/workspace/PageHeading'
import ResourceTabs from '../../components/workspace/ResourceTabs'
import StatePanel from '../../components/ui/StatePanel'
import Badge from '../../components/ui/Badge'
import WorkflowActions from '../../components/workspace/WorkflowActions'
export default function DetailPage({resource}) {
  const {id}=useParams();const {can,user}=useAuth();const location=useLocation();const {state,update}=useListState();const connected=resource.status==='connected'
  const load=useCallback((signal)=>serviceFor(resource).get(id,signal),[resource,id]);const result=useResource(load,connected&&can(resource.readPermission))
  if(!can(resource.readPermission))return <StatePanel state="denied"/>
  const tab=resource.tabs.includes(state.tab)?state.tab:resource.tabs[0]
  const canEdit=can(resource.updatePermission)&&(resource.id!=='roles'||user.roles.includes('Super Admin'))
  return <><PageHeading title={result.data?.name||resource.title} eyebrow={`${resource.group} / Record`} back={resource.path+location.search} description={`Reference: ${id}`}>{resource.writable&&canEdit&&<Link className="rounded-lg bg-teal-700 px-4 py-2.5 text-sm text-white" to={`${resource.path}/${id}/edit${location.search}`}>Edit record</Link>}</PageHeading><ResourceTabs tabs={resource.tabs} active={tab} onChange={(value)=>update({tab:value},false)}/>{connected&&result.status==='loading'?<StatePanel state="loading"/>:connected&&result.status==='error'?<StatePanel state={result.error.response?.status===403?'denied':'error'} onRetry={result.retry}>{result.error.userMessage||result.error.message}</StatePanel>:connected&&tab==='Overview'?<dl className="erp-panel grid gap-5 p-6 sm:grid-cols-2">{Object.entries(result.data).map(([key,value])=><div key={key} className={Array.isArray(value)?'sm:col-span-2':''}><dt className="text-xs text-slate-500">{label(key)}</dt><dd className="mt-1 break-words text-sm">{typeof value==='boolean'?<Badge status={value?'active':'disabled'}/>:Array.isArray(value)?<div className="mt-2 flex flex-wrap gap-2">{value.map((item)=><Badge key={item}>{item}</Badge>)}</div>:String(value)}</dd></div>)}</dl>:<StatePanel state="unavailable" title={`${tab} is not available`}>This section needs confirmed source records. No activity, costs or quantities are assumed.</StatePanel>}{!connected&&<WorkflowActions resource={resource}/>}</>
}
