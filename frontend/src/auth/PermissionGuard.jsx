import { useAuth } from './useAuth'
export default function PermissionGuard({ permission, children }) {
  const { can } = useAuth()
  return can(permission) ? children : <div role="alert"><h1 className="text-2xl font-semibold">Access restricted</h1><p className="mt-3 text-slate-500">Your role does not have permission to view this page.</p></div>
}
