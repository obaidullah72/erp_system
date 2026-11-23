import { useEffect, useId, useRef } from 'react'
import { X } from 'lucide-react'
export default function Modal({ open, onClose, title, children, drawer = false, id }) {
  const dialog = useRef(null)
  const close = useRef(onClose)
  const titleId = useId()
  useEffect(() => { close.current = onClose }, [onClose])
  useEffect(() => {
    const node = dialog.current
    if (!open) { if (node.open) node.close(); return }
    const previous = document.activeElement
    node.showModal()
    return () => { node.close(); previous?.focus?.() }
  }, [open])
  return <dialog id={id} ref={dialog} aria-labelledby={titleId} className={drawer ? 'erp-dialog erp-drawer' : 'erp-dialog'} onCancel={(event) => { event.preventDefault(); close.current() }} onClick={(event) => { if (event.target === event.currentTarget) close.current() }}>
    <div className="flex items-start justify-between gap-5 border-b border-slate-200 p-5 dark:border-slate-700"><h2 id={titleId} className="text-xl font-semibold">{title}</h2><button type="button" aria-label={`Close ${title}`} onClick={onClose} className="rounded-lg p-1 hover:bg-slate-100 dark:hover:bg-slate-800"><X size={22} /></button></div><div className="p-5">{children}</div>
  </dialog>
}
