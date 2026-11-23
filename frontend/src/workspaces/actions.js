const text = (name, label, required = true) => ({ name, label, required, type: 'text' })
const date = { name: 'accounting_date', label: 'Accounting date', type: 'date', required: true }
const amount = { name: 'amount', label: 'Amount', type: 'decimal', precision: 2, positive: true, required: true }
const reason = { name: 'reason', label: 'Reason', type: 'textarea', required: true }
const reference = (name, label) => ({ ...text(name, label), type: 'reference' })
export const actions = {
  archive: { label: 'Archive', grant: 'update', states: ['active'], fields: [reason] },
  approve: { label: 'Approve', grant: 'approve', states: ['draft', 'pending'], fields: [text('note', 'Approval note', false)] },
  post: { label: 'Post', grant: 'post', states: ['draft', 'approved'], fields: [date] },
  reverse: { label: 'Reverse', grant: 'reverse', states: ['posted'], fields: [date, reason] },
  cancel: { label: 'Cancel', grant: 'update', states: ['draft', 'pending', 'approved'], fields: [reason] },
  receive: { label: 'Receive goods', grant: 'post', states: ['approved', 'partially_received', 'dispatched'], fields: [reference('source_line_id', 'Order or transfer line'), reference('warehouse_id', 'Receiving warehouse'), { name: 'quantity', label: 'Quantity to receive', type: 'decimal', precision: 6, positive: true, required: true }, text('unit', 'Unit'), date] },
  dispatch: { label: 'Dispatch transfer', grant: 'post', states: ['approved'], fields: [date, reference('warehouse_id', 'Dispatch warehouse')] },
  pay: { label: 'Record payment', grant: 'post', states: ['posted', 'partially_paid'], fields: [amount, text('currency', 'Currency'), reference('account_id', 'Cash or bank account'), date, text('payment_reference', 'Payment reference')] },
  refund: { label: 'Refund payment', grant: 'reverse', states: ['posted', 'approved'], fields: [reference('original_payment_id', 'Original payment'), amount, date, reason] },
  allocate: { label: 'Allocate payment or cost', grant: 'post', states: ['draft', 'posted', 'partially_paid'], fields: [reference('source_id', 'Payment or cost source'), reference('target_id', 'Invoice or work order'), amount, date] },
  release: { label: 'Release', grant: 'approve', states: ['draft', 'approved', 'active'], fields: [date, reason] },
  fulfill: { label: 'Fulfill order', grant: 'post', states: ['approved', 'partially_fulfilled'], fields: [reference('shipment_id', 'Shipment'), date] },
  credit_check: { label: 'Check credit eligibility', grant: 'read', states: ['draft', 'pending'], fields: [reference('customer_id', 'Customer'), amount] },
  review: { label: 'Review variance', grant: 'approve', states: ['pending', 'draft'], fields: [reason] },
  match: { label: 'Match records', grant: 'update', states: ['draft', 'pending'], fields: [reference('source_id', 'Receipt or bank transaction'), reference('target_id', 'Invoice or ledger entry'), amount] },
  reconcile: { label: 'Reconcile', grant: 'approve', states: ['draft', 'pending'], fields: [date, reason] },
  import: { label: 'Import statement', grant: 'create', states: ['draft'], fields: [reference('bank_account_id', 'Bank account'), date] },
  open: { label: 'Open session', grant: 'create', states: ['draft'], fields: [amount, date] },
  close: { label: 'Close', grant: 'approve', states: ['open', 'completed', 'in_progress'], fields: [date, reason] },
  reopen: { label: 'Reopen period', grant: 'approve', states: ['soft_closed', 'locked'], fields: [reason] },
  retire: { label: 'Retire BOM revision', grant: 'approve', states: ['approved'], fields: [reason] },
  schedule: { label: 'Schedule order', grant: 'update', states: ['draft', 'released'], fields: [reference('resource_id', 'Resource'), { ...date, name: 'date_from', label: 'Start date' }, { ...date, name: 'date_to', label: 'End date' }] },
  consume: { label: 'Consume material', grant: 'post', states: ['released', 'in_progress'], fields: [reference('material_id', 'Material'), reference('batch_id', 'Source batch'), { name: 'quantity', label: 'Consumed quantity', type: 'decimal', positive: true, precision: 6, required: true }, text('unit', 'Unit'), date] },
  complete: { label: 'Record partial or final output', grant: 'post', states: ['released', 'in_progress'], fields: [reference('batch_id', 'Finished batch'), { name: 'quantity', label: 'Produced quantity', type: 'decimal', positive: true, precision: 6, required: true }, text('unit', 'Unit'), date] },
  quality_release: { label: 'Release quality hold', grant: 'approve', states: ['pending', 'quarantine'], fields: [reference('inspection_id', 'Passing inspection'), reason] },
  reject: { label: 'Reject output', grant: 'approve', states: ['pending', 'quarantine'], fields: [reason] },
}
export const recordStates = ['draft', 'pending', 'approved', 'partially_received', 'partially_fulfilled', 'partially_paid', 'posted', 'rejected', 'reversed', 'cancelled', 'completed', 'released', 'in_progress', 'active', 'disabled', 'dispatched', 'received', 'open', 'soft_closed', 'locked', 'quarantine', 'pass', 'fail', 'retired']
