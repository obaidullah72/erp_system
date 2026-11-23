import { api } from '../lib/axios'

export class CapabilityUnavailable extends Error {
  constructor(capability) { super(`${capability} is not available yet.`); this.code = 'capability_unavailable' }
}
// This is an explicit integration boundary, not a mock transport. Never request a planned route.
export function serviceFor(resource) {
  const pending = () => Promise.reject(new CapabilityUnavailable(resource.title))
  if (resource.status !== 'connected') return { list: pending, get: pending, create: pending, update: pending, archive: pending, action: pending, export: pending }
  const list = async (params = {}, signal) => {
    const accepted = resource.id === 'users' ? ['page', 'page_size', 'q', 'active'] : ['page', 'page_size']
    const query = Object.fromEntries(Object.entries(params).filter(([key, value]) => accepted.includes(key) && value !== '' && value != null))
    return (await api.get(resource.endpoint, { params: query, signal })).data
  }
  return {
    list,
    async get(id, signal) {
      // Stage 1 has no GET /users/:id or /roles/:id. Traverse its supported list contract.
      for (let page = 1; ; page++) {
        const data = await list({ page, page_size: 100 }, signal)
        const record = data.items.find((item) => item.id === id)
        if (record) return record
        if (page * 100 >= data.total) { const error = new Error('Record not found.'); error.status = 404; throw error }
      }
    },
    async create(payload) { return (await api.post(resource.endpoint, payload)).data },
    async update(id, payload) { return (await api.patch(`${resource.endpoint}/${encodeURIComponent(id)}`, payload)).data },
    archive: pending, action: pending, export: pending,
  }
}
export const settingsService = {
  async get(signal) { return (await api.get('/business-settings', { signal })).data },
  async update(payload) { return (await api.patch('/business-settings', payload)).data },
}
export const permissionService = { async list(signal) { return (await api.get('/roles/permissions', { signal })).data } }
