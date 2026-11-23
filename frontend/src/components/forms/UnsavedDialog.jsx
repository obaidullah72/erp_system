import ConfirmDialog from '../ui/ConfirmDialog'
export default function UnsavedDialog({ blocker }) {
  return <ConfirmDialog open={blocker.state === 'blocked'} title="Discard unsaved changes?" confirmLabel="Discard changes" onCancel={() => blocker.reset?.()} onConfirm={() => blocker.proceed?.()}>Your unsaved input will be lost. Stay here to continue editing.</ConfirmDialog>
}
