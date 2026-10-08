import { defineConfig } from '@playwright/test'
import { mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

// Backend aislado: BD propia en frontend/.e2e-run (no toca prestamos.db real ni backend/.env).
// Requiere `npm run build` antes (el backend sirve frontend/dist).
const runDir = fileURLToPath(new URL('./.e2e-run', import.meta.url))
mkdirSync(runDir, { recursive: true })

export const E2E_ADMIN = { usuario: 'jugarciamar', password: 'E2e-Prueba-2026' } // solo para la BD de pruebas

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  workers: 1,
  use: { baseURL: 'http://127.0.0.1:8766', trace: 'retain-on-failure' },
  webServer: {
    command: `python -m uvicorn app.main:app --app-dir ../../backend --host 127.0.0.1 --port 8766`,
    cwd: runDir,
    url: 'http://127.0.0.1:8766/health',
    reuseExistingServer: false,
    timeout: 60_000,
    env: {
      DATABASE_URL: 'sqlite:///./e2e.db',
      SECRET_KEY: 'e2e-secret-no-usar-en-produccion',
      DEFAULT_ADMIN_PASSWORD: E2E_ADMIN.password,
      ENABLE_DOCS: 'false',
      CORS_ORIGINS: 'http://127.0.0.1:8766',
    },
  },
})
