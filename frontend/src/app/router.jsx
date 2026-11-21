import { createBrowserRouter } from 'react-router-dom'
import DashboardLayout from '../layouts/DashboardLayout'
import AuthLayout from '../layouts/AuthLayout'
import ProtectedRoute from '../auth/ProtectedRoute'
import SystemStatusPage from '../pages/SystemStatusPage'
import DashboardPage from '../pages/DashboardPage'
import LoginPage from '../pages/LoginPage'
import RoadmapPage from '../pages/RoadmapPage'
import NotFoundPage from '../pages/NotFoundPage'
import ErrorPage from '../pages/ErrorPage'

export const router = createBrowserRouter([
  { element: <AuthLayout />, errorElement: <ErrorPage />, children: [{ path: '/login', element: <LoginPage /> }] },
  { element: <ProtectedRoute />, errorElement: <ErrorPage />, children: [{ element: <DashboardLayout />, children: [
    { path: '/', element: <DashboardPage /> },
    { path: '/system', element: <SystemStatusPage /> },
    { path: '/roadmap', element: <RoadmapPage /> },
    { path: '*', element: <NotFoundPage /> },
  ] }] },
])
