import { useState, useEffect } from 'react'
import { configService, type ConfigData } from '@/services/config.service'

export default function ConfigurationPage() {
  const [config, setConfig] = useState<ConfigData | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const [form, setForm] = useState<Record<string, string>>({})

  useEffect(() => {
    configService.get().then((res) => {
      if (res.success && res.data) {
        setConfig(res.data)
        const init: Record<string, string> = {}
        for (const [k, v] of Object.entries(res.data)) {
          init[k] = v === null || v === undefined ? '' : String(v)
        }
        setForm(init)
      } else {
        setErrorMsg('No se pudo cargar la configuración.')
      }
      setLoading(false)
    }).catch((err) => {
      setErrorMsg(err?.response?.data?.detail || err?.message || 'Error de conexión con el servidor.')
      setLoading(false)
    })
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccess('')
    setSaving(true)
    try {
      const payload: Record<string, any> = {}
      for (const k of ['empresa', 'nit', 'direccion', 'telefono', 'correo', 'logo', 'ruta_recibos', 'ruta_backups']) {
        if (form[k] !== String(config?.[k as keyof ConfigData] ?? '')) payload[k] = form[k] || null
      }
      for (const k of ['tasa_interes', 'dias_gracia', 'siguiente_factura']) {
        const v = form[k]
        if (v !== String(config?.[k as keyof ConfigData] ?? '')) {
          payload[k] = k === 'tasa_interes' ? parseFloat(v) : parseInt(v, 10)
        }
      }
      if (Object.keys(payload).length === 0) { setSuccess('Sin cambios.'); return }
      const res = await configService.update(payload)
      if (res.success) {
        setSuccess('Configuración guardada correctamente.')
        if (res.data) setConfig(res.data)
      }
    } catch {
      setSuccess('Error al guardar.')
    } finally {
      setSaving(false)
    }
  }

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement>) => setForm({ ...form, [k]: e.target.value })

  if (loading) return <div className="p-6 text-center text-gray-500">Cargando...</div>
  if (!config) return <div className="p-6 text-center text-red-500">{errorMsg || 'Error al cargar configuración.'}</div>

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="mb-6 text-2xl font-bold text-gray-800">Configuración</h1>

      {success && <div className={`mb-4 rounded-md p-3 text-sm ${success.includes('Error') ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>{success}</div>}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="rounded-lg bg-white p-4 shadow">
          <h3 className="mb-3 text-sm font-semibold text-gray-500 uppercase">Datos de la Empresa</h3>
          <div className="space-y-3">
            {[
              ['empresa', 'Nombre', 'text'],
              ['nit', 'NIT', 'text'],
              ['direccion', 'Dirección', 'text'],
              ['telefono', 'Teléfono', 'text'],
              ['correo', 'Correo', 'email'],
            ].map(([k, label, type]) => (
              <div key={k}>
                <label className="block text-sm font-medium text-gray-700">{label}</label>
                <input type={type} value={form[k] || ''} onChange={set(k)} className="mt-1 w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-lg bg-white p-4 shadow">
          <h3 className="mb-3 text-sm font-semibold text-gray-500 uppercase">Parámetros Financieros</h3>
          <div className="grid grid-cols-3 gap-3">
            {[
              ['tasa_interes', 'Tasa Interés %', 'number', '0.01'],
              ['dias_gracia', 'Días Gracia', 'number', '1'],
              ['siguiente_factura', 'Siguiente Factura', 'number', '1'],
            ].map(([k, label, type, step]) => (
              <div key={k}>
                <label className="block text-sm font-medium text-gray-700">{label}</label>
                <input type={type} step={step} value={form[k] || ''} onChange={set(k)} className="mt-1 w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-lg bg-white p-4 shadow">
          <h3 className="mb-3 text-sm font-semibold text-gray-500 uppercase">Rutas</h3>
          <div className="space-y-3">
            {[
              ['ruta_recibos', 'Carpeta de Recibos'],
              ['ruta_backups', 'Carpeta de Respaldos'],
            ].map(([k, label]) => (
              <div key={k}>
                <label className="block text-sm font-medium text-gray-700">{label}</label>
                <input type="text" value={form[k] || ''} onChange={set(k)} className="mt-1 w-full rounded-md border bg-gray-50 px-3 py-2 text-sm text-gray-500 outline-none" />
              </div>
            ))}
          </div>
        </div>

        <button type="submit" disabled={saving} className="w-full rounded-md bg-blue-600 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">
          {saving ? 'Guardando...' : 'Guardar Configuración'}
        </button>
      </form>
    </div>
  )
}
