import { Link } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { useListState } from '../../hooks/useListState'
import { resources } from '../../workspaces/catalog'
import PageHeading from '../../components/workspace/PageHeading'
import Badge from '../../components/ui/Badge'
import StatePanel from '../../components/ui/StatePanel'
export default function GroupPage({group}) {
  const {can}=useAuth();const {state,update}=useListState()
  const permitted=resources.filter((resource)=>resource.group===group&&can(resource.readPermission))
  const visible=permitted.filter((resource)=>`${resource.title} ${resource.family||''}`.toLowerCase().includes(state.q.toLowerCase()))
  return <><PageHeading title={group} eyebrow="TradeCore workspace" description={group==='Reports'?'Choose a specific report, reporting period and supporting records. Results remain unavailable until the underlying services are connected.':'Choose a workspace to view records, prepare input or manage business activity.'}/><label className="mb-6 block max-w-md text-sm">Find a workspace<input className="erp-input mt-2" value={state.q} onChange={(event)=>update({q:event.target.value})} placeholder={`Search ${group.toLowerCase()}…`}/></label>{!permitted.length?<StatePanel state="denied"/>:!visible.length?<StatePanel state="empty">No workspaces match this search.</StatePanel>:<div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{visible.map((resource)=><Link key={resource.id} to={resource.path} className="erp-panel block p-5 transition hover:border-teal-500 hover:shadow-sm"><div className="mb-4 flex items-center justify-between gap-2"><span className="text-xs uppercase tracking-wide text-slate-500">{resource.family||resource.kind}</span><Badge>{resource.status==='connected'?'Connected':'Unavailable'}</Badge></div><h2 className="font-semibold">{resource.title}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{resource.kind==='report'?`${resource.columns.slice(0,4).map((value)=>value.replaceAll('_',' ')).join(', ')} and supporting records.`:resource.status==='connected'?'View and manage confirmed records.':'Browse the workspace and review required inputs.'}</p></Link>)}</div>}</>
}
