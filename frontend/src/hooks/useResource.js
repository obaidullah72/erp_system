import { useEffect, useState } from 'react'
export function useResource(load, enabled = true) {
  const [state, setState] = useState({ status: 'loading', data: null, error: null })
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    if (!enabled) return
    const controller = new AbortController()
    let active = true
    Promise.resolve().then(() => { if (active) setState({ status: 'loading', data: null, error: null }); return load(controller.signal) })
      .then((data) => { if (active) setState({ status: 'ready', data, error: null }) })
      .catch((error) => { if (active && error.code !== 'ERR_CANCELED') setState({ status: 'error', data: null, error }) })
    return () => { active = false; controller.abort() }
  }, [load, enabled, attempt])
  return { ...state, retry: () => setAttempt((value) => value + 1) }
}
