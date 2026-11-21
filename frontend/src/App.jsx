import AuthProvider from './auth/AuthProvider'
import { RouterProvider } from 'react-router-dom'
import { router } from './app/router'

export default function App() {
  return <AuthProvider><RouterProvider router={router} /></AuthProvider>
}
