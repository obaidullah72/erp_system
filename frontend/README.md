# Frontend foundation

React/Vite, Tailwind v4, React Router, Axios and shared UI controls. Install with `npm ci`; start with `npm run dev`. See the root README for migrations, first-admin bootstrap and API startup.

`/login` is public; `/`, `/system` and `/roadmap` use the authenticated dashboard shell. Login connects to FastAPI, preserves the requested protected destination, keeps access tokens only in memory and restores sessions through the HttpOnly refresh cookie. Logout revokes the server session. Themes persist locally; mobile navigation collapses after selection. The dashboard explicitly marks unimplemented transaction metrics unavailable.

`npm run lint` and `npm run build` verify source/assets. `npm run test:e2e` requires ERP_TEST_DATABASE_URL pointing to a dedicated *_test PostgreSQL database. It starts isolated API/Vite servers and checks desktop/mobile flows. Install Chromium with `npx playwright install chromium`, or set PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH on hosts where that download is unsupported; details are in docs/testing.md.

Vite proxies `/api` to port 8000; container Nginx proxies to the API service. `npm run preview` only serves built static assets and does not provide that API proxy. VITE_API_URL is public build configuration. Keep a same-origin deployment for refresh-cookie compatibility. System status loads its chart code separately from login/dashboard.
