import axios from 'axios'
import { env } from '../config/env'

export const api = axios.create({ baseURL: env.apiUrl, timeout: 10000, withCredentials: true,
  headers: { Accept: 'application/json', 'X-ERP-CSRF': '1' } })
const sessionApi = axios.create({ baseURL: env.apiUrl, timeout: 10000, withCredentials: true,
  headers: { 'X-ERP-CSRF': '1' } })
let token = null
let refreshing = null
const listeners = new Set()
export function onSessionChange(listener) { listeners.add(listener); return () => listeners.delete(listener) }
export function setSession(data) {
  token = data?.access_token || null
  listeners.forEach((listener) => listener(data?.user || null))
}
export function refreshSession() {
  const request = () => sessionApi.post('/auth/refresh')
  if (!refreshing) refreshing = (navigator.locks ? navigator.locks.request('erp-session-refresh', request) : request()).then(({ data }) => {
    setSession(data)
    return data
  }).catch((error) => { setSession(null); throw error }).finally(() => { refreshing = null })
  return refreshing
}
api.interceptors.request.use((config) => {
  if (token) config.headers.Authorization = `Bearer ${token}`
  else delete config.headers.Authorization
  return config
})
api.interceptors.response.use((response) => response, async (error) => {
  const original = error.config
  if (error.response?.status === 401 && original && !original._retried && !original.url.startsWith('/auth/')) {
    original._retried = true
    try { await refreshSession(); return api(original) } catch { /* Sign-in state cleared. */ }
  }
  error.userMessage = error.response?.data?.error?.message || (error.code === 'ECONNABORTED'
    ? 'The API request timed out.' : error.response ? `Request failed (${error.response.status}).` : 'Unable to reach the API.')
  error.requestId = error.response?.headers?.['x-request-id']
  return Promise.reject(error)
})
