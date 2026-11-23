# Routes
/login: AuthLayout/LoginPage; /: DashboardLayout/DashboardPage; /system: SystemStatusPage; /roadmap: RoadmapPage. ProtectedRoute wraps workspace.
## router
Source: `frontend/src/app/router.jsx`

```jsx
import { createBrowserRouter } from 'react-router-dom'
import DashboardLayout from '../layouts/DashboardLayout'
import AuthLayout from '../layouts/AuthLayout'
import ProtectedRoute from '../auth/ProtectedRoute'
import DashboardPage from '../pages/DashboardPage'
import LoginPage from '../pages/LoginPage'
import RoadmapPage from '../pages/RoadmapPage'
import NotFoundPage from '../pages/NotFoundPage'
import ErrorPage from '../pages/ErrorPage'

export const router = createBrowserRouter([
  { element: <AuthLayout />, errorElement: <ErrorPage />, children: [{ path: '/login', element: <LoginPage /> }] },
  { element: <ProtectedRoute />, hydrateFallbackElement: <p className="p-8" role="status">Loading workspace…</p>, errorElement: <ErrorPage />, children: [{ element: <DashboardLayout />, children: [
    { path: '/', element: <DashboardPage /> },
    { path: '/system', lazy: async () => ({ Component: (await import('../pages/SystemStatusPage')).default }) },
    { path: '/roadmap', element: <RoadmapPage /> },
    { path: '*', element: <NotFoundPage /> },
  ] }] },
])

```