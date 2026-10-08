import { test, expect, type Page } from '@playwright/test'
import { E2E_ADMIN } from '../playwright.config'

const hoy = new Date().toISOString().slice(0, 10)
const unico = Date.now().toString().slice(-6)

async function login(page: Page, usuario = E2E_ADMIN.usuario, password = E2E_ADMIN.password) {
  await page.goto('/login')
  await page.locator('input[autocomplete="username"]').fill(usuario)
  await page.locator('input[autocomplete="current-password"]').fill(password)
  await page.getByRole('button', { name: 'Ingresar' }).click()
}

test('login con contraseña incorrecta muestra error', async ({ page }) => {
  await login(page, E2E_ADMIN.usuario, 'incorrecta')
  await expect(page.locator('.bg-red-50')).toBeVisible()
  await expect(page).toHaveURL(/\/login/)
})

test('rutas protegidas redirigen a login', async ({ page }) => {
  await page.goto('/clientes')
  await expect(page).toHaveURL(/\/login/)
})

test('flujo completo: cliente → buscar → pagar → recibo', async ({ page }) => {
  await login(page)
  await expect(page).toHaveURL(/\/$/)

  // Crear cliente + préstamo por API con el token de la sesión
  const token = await page.evaluate(() => localStorage.getItem('access_token'))
  const headers = { Authorization: `Bearer ${token}` }
  const placa = `E2E${unico}`
  const cr = await page.request.post('/api/v1/clientes', {
    headers,
    data: {
      nombre: `Cliente E2E ${unico}`, cedula: `9${unico}`, placa,
      capital_inicial: 30_000_000, valor_cuota: 1_200_000,
      fecha_inicio: hoy, fecha_primer_pago: hoy,
    },
  })
  expect(cr.status()).toBe(201)
  const clienteId = (await cr.json()).data.cliente.id
  const prestamoId = (await (await page.request.get(`/api/v1/clientes/${clienteId}`, { headers })).json()).data.prestamo.id

  // Búsqueda en la lista mientras se escribe
  await page.goto('/clientes')
  await page.getByPlaceholder('Buscar por placa, nombre o cédula...').fill(placa)
  await expect(page.getByText(`Cliente E2E ${unico}`)).toBeVisible()

  // Registrar pago: el formulario precarga cuota y fecha, y calcula
  await page.goto(`/prestamos/${prestamoId}/pagar`)
  const resumen = page.locator('text=Resumen del Cálculo').locator('..')
  await expect(resumen).toContainText('$750.000') // 30.000.000 × 2.5 %
  await expect(resumen).toContainText('$450.000')
  await expect(resumen).toContainText('$29.550.000')

  await page.getByRole('button', { name: 'Pagar y Generar Factura' }).click()
  await page.getByRole('button', { name: 'Confirmar Pago' }).click()
  await expect(page.getByRole('heading', { name: 'Pago Registrado' })).toBeVisible()
  await expect(page.getByText(/FACT-\d{6}/)).toBeVisible()

  await page.getByRole('button', { name: 'Ver Recibo' }).click()
  await expect(page).toHaveURL(/\/facturas\/\d+/)
  await expect(page.getByText(/FACT-\d{6}/).first()).toBeVisible()

  // Cartera mensual (reemplazo del bloque CXCOBRAR): el préstamo aparece como "Pagó" este mes
  await page.goto('/reportes')
  await expect(page.getByRole('button', { name: 'Cartera mensual' })).toBeVisible()
  const fila = page.getByRole('row').filter({ hasText: placa })
  await expect(fila).toContainText('Pagó')
  await expect(fila).toContainText('$29.550.000')
})
