import { createContext, useContext } from 'react'
export const NotificationContext = createContext({ notify: () => {} })
export const useNotification = () => useContext(NotificationContext)
