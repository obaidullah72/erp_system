import { createBrowserRouter } from 'react-router-dom'
import DashboardLayout from '../layouts/DashboardLayout'
import AuthLayout from '../layouts/AuthLayout'
import ProtectedRoute from '../auth/ProtectedRoute'
import DashboardPage from '../pages/DashboardPage'
import LoginPage from '../pages/LoginPage'
import RoadmapPage from '../pages/RoadmapPage'
import NotFoundPage from '../pages/NotFoundPage'
import ErrorPage from '../pages/ErrorPage'
import ResourcePage from '../pages/workspaces/ResourcePage'
import DetailPage from '../pages/workspaces/DetailPage'
import DraftPage from '../pages/workspaces/DraftPage'
import GroupPage from '../pages/workspaces/GroupPage'
import AdminEditorPage from '../pages/admin/AdminEditorPage'
import SettingsPage from '../pages/admin/SettingsPage'
import { resources, groups, groupSlug } from '../workspaces/catalog'
const resourceRoutes=resources.flatMap((resource)=>resource.id==='business-settings'?[{path:resource.path,element:<SettingsPage/>}]:[
  {path:resource.path,element:<ResourcePage resource={resource}/>},
  ...(resource.writable?[{path:resource.path+'/new',element:resource.status==='connected'?<AdminEditorPage resource={resource}/>:<DraftPage resource={resource}/>},{path:resource.path+'/:id/edit',element:resource.status==='connected'?<AdminEditorPage resource={resource}/>:<DraftPage resource={resource}/>}]:[]),
  {path:resource.path+'/:id',element:<DetailPage resource={resource}/>},
])
export const router=createBrowserRouter([
  {element:<AuthLayout/>,errorElement:<ErrorPage/>,children:[{path:'/login',element:<LoginPage/>}]},
  {element:<ProtectedRoute/>,hydrateFallbackElement:<p className="p-8" role="status">Loading workspace…</p>,errorElement:<ErrorPage/>,children:[{element:<DashboardLayout/>,children:[
    {path:'/',element:<DashboardPage/>},
    ...groups.map((group)=>({path:'/workspace/'+groupSlug(group),element:<GroupPage group={group}/>})),
    ...resourceRoutes,
    {path:'/system',lazy:async()=>({Component:(await import('../pages/SystemStatusPage')).default})},
    {path:'/roadmap',element:<RoadmapPage/>},
    {path:'*',element:<NotFoundPage/>},
  ]}]},
])
