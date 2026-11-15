# Frontend foundation

React + Vite, JavaScript, Tailwind CSS v4 (Vite plugin and CSS import), React Router DOM, Axios, React Hook Form, Zod, Recharts, and Lucide React.

Run `npm install`, then `npm run dev` from this directory. See the root README for backend/database setup. `npm run build` creates `dist`; `npm run preview` only serves static output and does not provide the development API proxy. Use Compose Nginx or a separately configured `VITE_API_URL` for API access from the built app.

Routes: `/system` (real health checks), `/foundation` (scope and memory-only validation form), `/roadmap` (planned phases). No business dashboards or simulated records. Chart samples exist only in page memory; failures are gaps, never zero-duration successes.
