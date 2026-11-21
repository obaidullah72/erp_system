import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: './tests/e2e', fullyParallel: false, workers: 1,
  use: { baseURL: 'http://127.0.0.1:5174', browserName: 'chromium', headless: true,
    screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  webServer: [
    { command: '../backend/venv/bin/python ../backend/scripts/e2e_server.py',
      url: 'http://127.0.0.1:8001/api/v1/health/ready', reuseExistingServer: false, timeout: 30000 },
    { command: 'npm run dev -- --host 127.0.0.1 --port 5174',
      env: { ERP_API_PROXY_TARGET: 'http://127.0.0.1:8001' },
      url: 'http://127.0.0.1:5174', reuseExistingServer: false, timeout: 30000 },
  ],
})
