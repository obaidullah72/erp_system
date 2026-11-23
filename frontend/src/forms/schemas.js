import { z } from 'zod'

export function fieldSchema(field) {
  let schema = z.string()
  if (field.required) schema = schema.trim().min(1, `${field.label} is required`)
  if (field.type === 'email') schema = schema.refine((v) => !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), 'Enter a valid email address')
  if (field.type === 'reference') schema = schema.refine((v) => !v || /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(v), 'Enter a valid record UUID')
  if (field.type === 'decimal') schema = schema.refine((v) => {
    if (!v) return !field.required
    if (!new RegExp(`^\\d{1,14}(?:\\.\\d{1,${field.precision || 6}})?$`).test(v)) return false
    return !field.positive || /[1-9]/.test(v)
  }, `Enter ${field.positive ? 'a positive' : 'a nonnegative'} decimal with up to ${field.precision || 6} places`)
  if (field.type === 'integer') schema = schema.refine((v) => !v && !field.required || /^\d+$/.test(v) && Number(v) >= (field.min ?? 0) && Number(v) <= (field.max ?? 1000000), `Enter a whole number between ${field.min ?? 0} and ${field.max ?? 1000000}`)
  if (field.type === 'date') schema = schema.refine((v) => !v && !field.required || /^\d{4}-\d{2}-\d{2}$/.test(v) && !Number.isNaN(Date.parse(v)) && new Date(v).toISOString().slice(0, 10) === v, 'Enter a valid date')
  if (field.pattern === 'currency') schema = schema.refine((v) => /^[A-Z]{3}$/.test(v), 'Use a three-letter currency code')
  if (field.type === 'select') schema = schema.refine((v) => !v && !field.required || field.options.includes(v), 'Choose a listed option')
  return schema
}
export function schemaFor(fields, lines) {
  const shape = Object.fromEntries(fields.map((field) => [field.name, fieldSchema(field)]))
  if (lines) shape.lines = z.array(z.object(Object.fromEntries(lines.map((field) => [field.name, fieldSchema(field)])))).min(1, 'Add at least one line')
  return z.object(shape).superRefine((data, context) => {
    const issue = (path, message) => context.addIssue({ code: 'custom', path: [path], message })
    if (data.invoice_date && data.due_date && data.invoice_date > data.due_date) issue('due_date', 'Due date must be on or after invoice date')
    if (data.date_from && data.date_to && data.date_from > data.date_to) issue('date_to', 'End date must be on or after start date')
    if (data.from_warehouse_id && data.from_warehouse_id === data.to_warehouse_id) issue('to_warehouse_id', 'Choose a different destination warehouse')
    if (data.from_account_id && data.from_account_id === data.to_account_id) issue('to_account_id', 'Choose a different destination account')
    if (data.from_unit && data.from_unit === data.to_unit) issue('to_unit', 'Choose a different target unit')
    if (data.manufactured_on && data.expires_on && data.manufactured_on > data.expires_on) issue('expires_on', 'Expiry must not precede manufacture')
  })
}
export const defaultsFor = (fields) => Object.fromEntries(fields.map((field) => [field.name, '']))
export const userSchema = (editing) => z.object({
  name: z.string().trim().min(1, 'Name is required').max(160),
  email: editing ? z.string() : z.email('Enter a valid email address').max(254),
  password: editing ? z.union([z.literal(''), z.string().min(12, 'Use at least 12 characters').max(256)]) : z.string().min(12, 'Use at least 12 characters').max(256),
  role_ids: z.array(z.string()), active: z.boolean(),
})
export const roleSchema = z.object({ name: z.string().regex(/^[A-Za-z][A-Za-z0-9 _-]*$/, 'Start with a letter; use letters, numbers, spaces, underscores or hyphens').max(80), permissions: z.array(z.string()) })
export const businessSettingsSchema = z.object({ currency: z.string().regex(/^[A-Z]{3}$/, 'Use a three-letter currency code'), timezone: z.string().min(1).refine((value) => { try { new Intl.DateTimeFormat('en', { timeZone: value }); return true } catch { return false } }, 'Enter a valid IANA timezone') })
export function applyBackendErrors(error, setError) {
  for (const detail of error.response?.data?.error?.details || []) {
    const path = detail.location?.filter((part) => part !== 'body').join('.')
    if (path) setError(path, { type: 'server', message: `The server rejected this field (${detail.type}). Review its value.` })
  }
}
