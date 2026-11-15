import { createBrowserRouter, Navigate } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import SystemStatusPage from '../pages/SystemStatusPage'
import FoundationPage from '../pages/FoundationPage'
import RoadmapPage from '../pages/RoadmapPage'
import NotFoundPage from '../pages/NotFoundPage'
import ErrorPage from '../pages/ErrorPage'

export const router = createBrowserRouter([{
  element: <AppLayout />, errorElement: <ErrorPage />, children: [
    { path: '/', element: <Navigate to="/system" replace /> },
    { path: '/system', element: <SystemStatusPage /> },
    { path: '/foundation', element: <FoundationPage /> },
    { path: '/roadmap', element: <RoadmapPage /> },
    { path: '*', element: <NotFoundPage /> },
  ],
}])
