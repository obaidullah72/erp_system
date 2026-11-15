import axios from 'axios'
import { env } from '../config/env'

export const api = axios.create({
  baseURL: env.apiUrl,
  timeout: 10000,
  headers: { Accept: 'application/json' },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    error.userMessage = error.response?.data?.error?.message
      || (error.code === 'ECONNABORTED' ? 'The API request timed out.'
        : error.response ? `The API returned HTTP ${error.response.status}.` : 'Unable to reach the API. Check that the backend is running.')
    error.requestId = error.response?.headers?.['x-request-id']
    return Promise.reject(error)
  },
)
