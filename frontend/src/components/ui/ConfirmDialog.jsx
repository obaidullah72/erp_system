import Modal from './Modal'
import Button from './Button'
export default function ConfirmDialog({ open, title = 'Confirm action', children, onCancel, onConfirm, pending = false, confirmLabel = 'Confirm' }) {
  return <Modal open={open} title={title} onClose={pending ? () => {} : onCancel}><div className="text-sm leading-6">{children}</div><div className="mt-6 flex justify-end gap-3"><Button type="button" variant="secondary" onClick={onCancel} disabled={pending}>Cancel</Button><Button type="button" onClick={onConfirm} disabled={pending}>{pending ? 'Working…' : confirmLabel}</Button></div></Modal>
}
