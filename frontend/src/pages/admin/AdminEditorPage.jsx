import { useCallback } from 'react'
import { useParams } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { useResource } from '../../hooks/useResource'
import { serviceFor, permissionService } from '../../services/resources'
import { resourceById } from '../../workspaces/catalog'
import PageHeading from '../../components/workspace/PageHeading'
import StatePanel from '../../components/ui/StatePanel'
import AdminForm from './AdminForm'
export default function AdminEditorPage({resource}) {
  const {id}=useParams()
  const {can,user}=useAuth()
  const permitted=can(id ? resource.updatePermission : resource.createPermission) && (resource.id!=='roles' || user.roles.includes('Super Admin'))
  const load=useCallback(async(signal)=>{
    const [record,options]=await Promise.all([id ? serviceFor(resource).get(id,signal) : Promise.resolve(null),resource.id==='users' ? (async()=>{const service=serviceFor(resourceById.roles);let items=[];for(let page=1;;page++){const result=await service.list({page,page_size:100},signal);items=items.concat(result.items);if(items.length>=result.total)return items}})() : permissionService.list(signal)])
    return {record,options}
  },[id,resource])
  const result=useResource(load,permitted)
  if(!permitted)return <StatePanel state="denied">This action requires an authorized administrator.</StatePanel>
  return <><PageHeading title={`${id?'Edit':'Create'} ${resource.id==='users'?'user':'role'}`} eyebrow="Administration" back={resource.path} description="Changes are sent to the server and confirmed before success is shown." />{result.status==='loading'?<StatePanel state="loading"/>:result.status==='error'?<StatePanel state={result.error.response?.status===403?'denied':'error'} onRetry={result.retry}>{result.error.userMessage||result.error.message}</StatePanel>:<AdminForm key={`${id||'new'}-${result.data.record?.version||0}`} resource={resource} record={result.data.record} roles={resource.id==='users'?result.data.options:[]} permissions={resource.id==='roles'?result.data.options:[]} />}</>
}
