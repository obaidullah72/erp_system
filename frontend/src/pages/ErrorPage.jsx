import { isRouteErrorResponse, useRouteError } from 'react-router-dom'
import ErrorState from '../components/ui/ErrorState'

export default function ErrorPage() {
  const error = useRouteError()
  return <main className="mx-auto max-w-xl p-8"><ErrorState title="This page could not be displayed" message={isRouteErrorResponse(error) ? `HTTP ${error.status}` : 'An unexpected interface error occurred.'} onRetry={() => window.location.reload()} /></main>
}
