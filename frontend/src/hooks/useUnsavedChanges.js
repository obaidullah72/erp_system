import { useBeforeUnload, useBlocker } from 'react-router-dom'
import { useCallback } from 'react'
export function useUnsavedChanges(dirty) {
  useBeforeUnload(useCallback((event) => { if (dirty) { event.preventDefault(); event.returnValue = '' } }, [dirty]))
  return useBlocker(({ currentLocation, nextLocation }) => dirty && currentLocation.pathname !== nextLocation.pathname)
}
