import { useState } from 'react'
import Button from '../ui/Button'
import StatePanel from '../ui/StatePanel'
// States are driven only by confirmed jobs. Pending contracts never call an export route.
export default function ExportPanel({ canExport, availability = 'pending', job = null, onRequest, onRetry, onDownload }) {
  const [format, setFormat] = useState('pdf')
  if (!canExport) return <StatePanel state="denied" title="Export access required">Ask an administrator for export access.</StatePanel>
  const pending = job?.status === 'queued' || job?.status === 'running'
  return <section className="erp-panel p-5" aria-label="Report export"><div className="flex flex-wrap items-end gap-3"><label className="text-sm">File format<select className="erp-input mt-1" value={format} onChange={(event) => setFormat(event.target.value)} disabled={pending}><option value="pdf">PDF</option><option value="xlsx">Excel (.xlsx)</option></select></label><Button disabled={availability !== 'connected' || pending} onClick={() => onRequest?.(format)}>{pending ? 'Preparing export…' : 'Export report'}</Button></div>{availability !== 'connected' && <p className="mt-3 text-sm text-slate-500">PDF and Excel exports are not available for this report yet.</p>}{pending && <div role="status" className="mt-4"><p>Preparing your requested export…</p><progress className="mt-2 w-full" aria-label="Export progress" max={100} value={job.progress ?? undefined} /></div>}{job?.status === 'failed' && <StatePanel state="error" title="Export failed" onRetry={onRetry}>{job.message || 'Your report could not be prepared. Your filters are preserved.'}</StatePanel>}{job?.status === 'ready' && <Button className="mt-3" disabled={!job.download_authorized} onClick={onDownload}>{job.download_authorized ? 'Download export' : 'Download access required'}</Button>}</section>
}
