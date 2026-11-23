# Tokens
React/Vite; Tailwind v4 Vite plugin; custom controls. Teal #0d806b/#096754; navy sidebar #122b32; slate backgrounds. Font Inter/system sans. Rounded lg/xl controls. sm/md/lg responsive breakpoints. Dark class persisted by erp-theme.
## index
Source: `frontend/src/index.css`

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));

:root { font-family: Inter, ui-sans-serif, system-ui, sans-serif; color: #172b3a; background: #f5f7fa; font-synthesis: none; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; }
:root.dark { color-scheme: dark; color: #e2e8f0; background: #0f172a; }
body { margin: 0; min-width: 320px; }
button, a, input { -webkit-tap-highlight-color: transparent; }
button { cursor: pointer; }
button:disabled { cursor: wait; }
:focus-visible { outline: 3px solid #14b8a6; outline-offset: 4px; }
@theme { --color-brand-50: #eefbf8; --color-brand-600: #0d806b; --color-brand-700: #096754; }

```

## useTheme
Source: `frontend/src/hooks/useTheme.js`

```js
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

```

## vite.config
Source: `frontend/vite.config.js`

```js
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: { '/api': { target: process.env.ERP_API_PROXY_TARGET || 'http://127.0.0.1:8000', changeOrigin: true } },
  },
})

```