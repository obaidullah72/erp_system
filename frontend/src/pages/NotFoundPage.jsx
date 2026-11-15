import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return <div className="py-16"><p className="text-sm font-semibold text-teal-600">404</p><h1 className="mt-3 text-3xl font-semibold">Page not found</h1><p className="mt-3 text-slate-500">This route is unavailable. Business modules are planned for later phases.</p><Link to="/system" className="mt-6 inline-block text-teal-600 underline">Return to system status</Link></div>
}
