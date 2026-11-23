import { useEffect, useId, useRef, useState } from 'react'
import { z } from 'zod'
const supported = ['image/png','image/jpeg','image/webp','application/pdf','text/csv','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
const fileSchema = z.custom((file) => file instanceof File && file.size <= 5 * 1024 * 1024 && supported.includes(file.type), 'Choose PNG, JPEG, WebP, PDF, CSV or XLSX files up to 5 MB.')
export default function AttachmentInput() {
  const id = useId()
  const [files, setFiles] = useState([])
  const [error, setError] = useState('')
  const urls = useRef([])
  useEffect(() => () => urls.current.forEach((url) => URL.revokeObjectURL(url)), [])
  function change(event) {
    const chosen = [...event.target.files]
    if (chosen.length > 10 || chosen.some((file) => !fileSchema.safeParse(file).success)) { setError('Choose up to 10 PNG, JPEG, WebP, PDF, CSV or XLSX files, each up to 5 MB.'); return }
    urls.current.forEach((url) => URL.revokeObjectURL(url))
    urls.current = chosen.map((file) => URL.createObjectURL(file))
    setFiles(chosen.map((file,index) => ({ name:file.name, image:file.type.startsWith('image/'), url:urls.current[index] }))); setError('')
  }
  return <section className="space-y-3"><label htmlFor={id} className="block text-sm font-medium">Images & supporting attachments</label><input id={id} type="file" multiple accept={supported.join(',')} onChange={change} aria-describedby={`${id}-help`} className="erp-input" /><p id={`${id}-help`} className="text-xs text-slate-500">Local preview only. Attachments cannot be uploaded until this workspace is available. Maximum 10 files, 5 MB each.</p>{error && <p role="alert" className="text-sm text-red-600">{error}</p>}<ul className="flex flex-wrap gap-3">{files.map((file,index) => <li key={index} className="max-w-40 rounded-lg border border-slate-200 p-2 text-xs dark:border-slate-700">{file.image && <img src={file.url} alt={`Preview of ${file.name}`} className="mb-2 h-24 w-32 object-contain" />}<span className="break-all">{file.name}</span></li>)}</ul></section>
}
