import { useEffect, useState } from 'react'

function initialTheme() {
  try {
    const saved = localStorage.getItem('erp-theme')
    if (saved === 'dark' || saved === 'light') return saved
  } catch { /* Theme still works when browser storage is unavailable. */ }
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export function useTheme() {
  const [theme, setTheme] = useState(initialTheme)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])
  function toggleTheme() {
    const next = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    try { localStorage.setItem('erp-theme', next) } catch { /* Storage is optional. */ }
  }
  return { theme, toggleTheme }
}
