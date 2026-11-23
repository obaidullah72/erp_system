import { useState } from 'react'
import { NotificationContext } from '../../hooks/useNotification'
export default function NotificationProvider({ children }) {
  const [message, setMessage] = useState(null)
  return <NotificationContext.Provider value={{ notify: (text) => setMessage(text) }}>{children}{message && <div role="status" className="fixed bottom-5 right-5 z-50 flex max-w-sm gap-4 rounded-xl bg-slate-900 p-4 text-sm text-white shadow-lg"><span>{message}</span><button onClick={() => setMessage(null)} aria-label="Dismiss notification">Dismiss</button></div>}</NotificationContext.Provider>
}
