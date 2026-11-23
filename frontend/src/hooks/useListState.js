import { useSearchParams } from 'react-router-dom'
export function useListState() {
  const [params, setParams] = useSearchParams()
  const integer = (name, fallback, max) => Math.min(max, Math.max(1, Number.parseInt(params.get(name), 10) || fallback))
  const state = { ...Object.fromEntries(params), q: params.get('q') || '', page: integer('page', 1, 100000), page_size: [10,25,50,100].includes(Number(params.get('page_size'))) ? Number(params.get('page_size')) : 25 }
  function update(patch, resetPage = true) {
    setParams((previous) => { const next = new URLSearchParams(previous); if (resetPage) next.set('page', '1'); Object.entries(patch).forEach(([key, value]) => value === '' || value == null ? next.delete(key) : next.set(key, String(value))); return next })
  }
  return { state, update }
}
