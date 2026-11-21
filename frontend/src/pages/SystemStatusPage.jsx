import { useEffect, useState } from 'react'
import { Activity, Database, RefreshCw, Server, CheckCircle2, CircleAlert, Clock3, ArrowUpRight } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../lib/axios'
import ErrorState from '../components/ui/ErrorState'

const panel = 'rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900'

async function probe(path, signal) {
  const start = performance.now()
  try {
    const response = await api.get(path, { signal })
    const valid = response.data?.status === 'ok' && response.data?.service === 'erp-api'
      && (path !== '/health/ready' || response.data?.database === 'connected')
    if (!valid) return { ok: false, message: 'Unexpected API response. Check the API URL.', latency: null }
    return { ok: true, latency: Math.round(performance.now() - start), requestId: response.headers['x-request-id'] }
  } catch (error) {
    if (signal.aborted) throw error
    return { ok: false, message: path === '/health/ready' && error.response?.status === 503
      ? 'The API is reachable, but PostgreSQL is not ready.' : error.userMessage || 'The request failed.', requestId: error.requestId, latency: null }
  }
}

function StatusCard({ title, icon: Icon, result, loading, description }) {
  const color = !result ? 'text-slate-500' : result.ok ? 'text-teal-700 dark:text-teal-300' : 'text-amber-700 dark:text-amber-300'
  return <section className={`${panel} p-6`}><div className="flex items-center justify-between"><span className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</span><Icon size={20} className="text-slate-400" /></div><div className={`mt-5 flex items-center gap-2 text-xl font-semibold ${color}`}>{loading ? <Clock3 size={20} /> : result?.ok ? <CheckCircle2 size={20} /> : <CircleAlert size={20} />}{loading ? 'Checking…' : !result ? 'Not checked' : result.ok ? 'Operational' : 'Unavailable'}</div><p className="mt-3 text-xs leading-5 text-slate-500 dark:text-slate-400">{result?.message || description}</p>{result?.ok && <p className="mt-3 text-xs text-slate-500">Observed response: {result.latency} ms</p>}</section>
}

export default function SystemStatusPage() {
  const [state, setState] = useState({ loading: true, live: null, ready: null, checkedAt: null })
  const [history, setHistory] = useState([])
  const [refreshIndex, setRefreshIndex] = useState(0)
  useEffect(() => {
    const controller = new AbortController()
    Promise.all([
      probe('/health/live', controller.signal),
      probe('/health/ready', controller.signal),
    ]).then(([live, ready]) => {
      if (controller.signal.aborted) return
      setState({ live, ready, loading: false, checkedAt: new Date() })
      setHistory(previous => [...previous.slice(-19), {
        sample: (previous.at(-1)?.sample || 0) + 1,
        api: live.latency,
        database: ready.latency,
      }])
    }).catch(() => { /* Cancelled requests cannot overwrite newer results. */ })
    return () => controller.abort()
  }, [refreshIndex])
  function handleRefresh() {
    setState(previous => ({ ...previous, loading: true }))
    setRefreshIndex(previous => previous + 1)
  }
  return <>
    <div className="mb-8 flex flex-wrap items-start justify-between gap-4"><div><p className="mb-2 text-xs font-semibold uppercase tracking-[.18em] text-teal-700 dark:text-teal-300">Platform / System health</p><h1 className="text-3xl font-semibold tracking-tight">System status</h1><p className="mt-3 text-sm text-slate-500 dark:text-slate-400">Live checks for the services behind your ERP workspace.</p></div><button onClick={handleRefresh} disabled={state.loading} className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-700 disabled:opacity-60"><RefreshCw size={16} className={state.loading ? 'animate-spin' : ''} />Refresh checks</button></div>
    <div className="mb-6 flex items-start gap-3 rounded-xl border border-teal-200 bg-teal-50 p-4 text-teal-900 dark:border-teal-900 dark:bg-teal-950 dark:text-teal-100"><Activity size={19} className="mt-0.5 shrink-0" /><div><p className="text-sm font-medium">Foundation environment</p><p className="mt-1 text-xs leading-5 opacity-80">These checks use the real API. Operational sales, inventory, accounting screens, and manufacturing are planned for later stages.</p></div></div>
    <div aria-live="polite" className="grid gap-5 md:grid-cols-2"><StatusCard title="API liveness" icon={Server} result={state.live} loading={state.loading} description="Confirms that the API process can respond." /><StatusCard title="Database readiness" icon={Database} result={state.ready} loading={state.loading} description="Confirms PostgreSQL connectivity with SELECT 1." /></div>
    {!state.loading && state.live && !state.live.ok && <div className="mt-5"><ErrorState title="API connection failed" message={state.live.message} requestId={state.live.requestId} onRetry={handleRefresh} /></div>}
    <section className={`${panel} mt-6 p-6`}><div className="flex flex-wrap justify-between gap-2"><div><h2 className="font-semibold">Observed response times</h2><p className="mt-1 text-xs text-slate-500">Actual browser requests from this session · latest 20 checks</p></div><span className="text-xs text-slate-500">{state.checkedAt ? `Last checked ${state.checkedAt.toLocaleTimeString()}` : 'Waiting for first check'}</span></div>
      {history.filter(sample => sample.api !== null || sample.database !== null).length < 2 ? <div className="flex h-44 flex-col items-center justify-center gap-3 text-center text-sm text-slate-500"><Activity size={26} className="text-slate-300" /><p>Run at least two successful checks to view response times.</p><p className="text-xs">Failed requests are not plotted as zero.</p></div> : <div className="mt-6 h-52" role="img" aria-label="Observed API and readiness response times in milliseconds"><ResponsiveContainer width="100%" height="100%"><LineChart data={history}><XAxis dataKey="sample" tick={{ fill: '#94a3b8', fontSize: 12 }} /><YAxis unit=" ms" width={65} tick={{ fill: '#94a3b8', fontSize: 12 }} /><Tooltip contentStyle={{ background: '#fff', color: '#172b3a', borderRadius: 8 }} /><Line name="API liveness (ms)" dataKey="api" stroke="#0d9488" strokeWidth={2} isAnimationActive={false} /><Line name="Database readiness (ms)" dataKey="database" stroke="#6366f1" strokeWidth={2} isAnimationActive={false} /></LineChart></ResponsiveContainer></div>}
      <p className="mt-3 text-xs leading-5 text-slate-500">Durations include browser, network, and API processing time. Readiness latency is not an isolated database benchmark. Refresh manually to collect another sample.</p>
    </section>
    <section className={`${panel} mt-6 p-6`}><h2 className="font-semibold">Health endpoint reference</h2><div className="mt-5 grid gap-5 text-sm sm:grid-cols-2"><div><code className="text-xs text-teal-700 dark:text-teal-300">GET /api/v1/health/live</code><p className="mt-2 text-xs text-slate-500">HTTP 200 while the API can respond. Independent of the database.</p></div><div><code className="text-xs text-teal-700 dark:text-teal-300">GET /api/v1/health/ready</code><p className="mt-2 text-xs text-slate-500">HTTP 200 when PostgreSQL responds; HTTP 503 when unavailable.</p></div></div><a href="/" className="mt-6 inline-flex items-center gap-1 text-xs font-medium text-teal-700 dark:text-teal-300">Back to dashboard<ArrowUpRight size={14} /></a></section>
  </>
}
