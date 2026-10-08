import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { prestamoService } from '@/services/prestamo.service'
import { clienteService, type ClienteListado } from '@/services/cliente.service'
import { useUnsaved } from '@/contexts/UnsavedContext'
import { useToast } from '@/contexts/ToastContext'
import CurrencyInput from '@/components/CurrencyInput'

export default function PrestamoFormPage() {
  const { setDirty } = useUnsaved()
  const { addToast } = useToast()
  const navigate = useNavigate()
  const [clientes, setClientes] = useState<ClienteListado[]>([])
  const [clienteSearch, setClienteSearch] = useState('')
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const today = new Date().toISOString().split('T')[0]
  const [form, setForm] = useState({
    cliente_id: '', capital_inicial: 0, valor_cuota: 0,
    fecha_inicio: today,
  })

  useEffect(() => {
    clienteService.list({ page_size: 500 }).then((res) => {
      if (res.success && res.data) setClientes(res.data.items.filter((c: ClienteListado) => c.estado === 'ACTIVO'))
    })
  }, [])

  const filtered = clientes.filter((c) =>
    !clienteSearch || c.nombre.toLowerCase().includes(clienteSearch.toLowerCase()) ||
    c.cedula.includes(clienteSearch) || c.placa.toLowerCase().includes(clienteSearch.toLowerCase())
  )

  const selectedCliente = clientes.find((c) => c.id === Number(form.cliente_id))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!form.cliente_id) { setError('Seleccione un cliente.'); return }
    if (!form.capital_inicial || !form.valor_cuota) { setError('Complete los campos obligatorios.'); return }
    if (form.capital_inicial <= 0 || form.valor_cuota <= 0) { setError('Los valores deben ser mayores a cero.'); return }
    setLoading(true)
    try {
      const res = await prestamoService.create({
        cliente_id: Number(form.cliente_id),
        capital_inicial: form.capital_inicial,
        valor_cuota: form.valor_cuota,
        fecha_inicio: form.fecha_inicio,
      })
      if (res.success && res.data) {
        setDirty()
        addToast('success', 'Préstamo creado correctamente')
        navigate(`/prestamos/${res.data.prestamo.id}`)
      } else setError('Error al crear el préstamo.')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Error al crear el préstamo.')
    } finally {
      setLoading(false)
    }
  }

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setForm({ ...form, [k]: e.target.value })

  return (
    <div className="p-6 lg:p-8 max-w-xl mx-auto animate-fade-in">
      <button onClick={() => navigate('/prestamos')} className="mb-4 text-sm text-primary-600 hover:text-primary-700 font-medium">&larr; Volver a Préstamos</button>
      <h1 className="page-title mb-6">Nuevo Préstamo</h1>

      {error && <div className="mb-4 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">{error}</div>}

      <form onSubmit={handleSubmit} className="card p-6 space-y-4">
        <div className="relative">
          <label className="block text-sm font-medium text-surface-700 mb-1">Cliente *</label>
          <input
            type="text" placeholder="Buscar cliente por nombre, cédula o placa..."
            value={clienteSearch} onChange={(e) => { setClienteSearch(e.target.value); setDropdownOpen(true) }}
            onFocus={() => setDropdownOpen(true)}
            className="input"
          />
          {selectedCliente && (
            <p className="mt-1 text-xs text-emerald-600 font-medium">Seleccionado: {selectedCliente.nombre} - {selectedCliente.cedula}</p>
          )}
          {dropdownOpen && (
            <div className="absolute z-10 mt-1 max-h-48 w-full overflow-y-auto rounded-xl border border-surface-200 bg-white shadow-lg animate-scale-in">
              {filtered.length === 0 ? (
                <div className="p-3 text-sm text-surface-400">Sin resultados.</div>
              ) : (
                filtered.map((c) => (
                  <button
                    type="button" key={c.id}
                    onClick={() => { setForm({ ...form, cliente_id: String(c.id) }); setClienteSearch(''); setDropdownOpen(false) }}
                    className={`w-full px-3 py-2.5 text-left text-sm transition-colors hover:bg-primary-50 ${
                      c.id === Number(form.cliente_id) ? 'bg-primary-50 font-medium text-primary-700' : 'text-surface-700'
                    }`}
                  >
                    <span className="font-medium">{c.nombre}</span>
                    <span className="ml-2 text-xs text-surface-400">{c.cedula} &middot; {c.placa}</span>
                  </button>
                ))
              )}
              <div className="border-t border-surface-100 p-2">
                <button type="button" onClick={() => { setDropdownOpen(false); navigate('/clientes/nuevo') }} className="w-full rounded-md px-2 py-1.5 text-xs text-primary-600 hover:bg-primary-50 font-medium text-center">
                  + Crear nuevo cliente
                </button>
              </div>
            </div>
          )}
        </div>

          <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-surface-700 mb-1">Capital Inicial *</label>
            <CurrencyInput value={form.capital_inicial} onChange={(v) => setForm((prev) => ({ ...prev, capital_inicial: v }))} className="input" />
          </div>
          <div>
            <label className="block text-sm font-medium text-surface-700 mb-1">Valor Cuota *</label>
            <CurrencyInput value={form.valor_cuota} onChange={(v) => setForm((prev) => ({ ...prev, valor_cuota: v }))} className="input" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1">Fecha de Inicio *</label>
          <input type="date" value={form.fecha_inicio} onChange={set('fecha_inicio')} className="input" />
          <p className="mt-1 text-xs text-surface-400">El primer pago se calculará automáticamente un mes después.</p>
        </div>

        <div className="flex gap-3 pt-2">
          <button type="button" onClick={() => navigate('/prestamos')} className="btn-secondary flex-1">Cancelar</button>
          <button type="submit" disabled={loading} className="btn-primary flex-1">
            {loading ? 'Creando...' : 'Crear Préstamo'}
          </button>
        </div>
      </form>
    </div>
  )
}
