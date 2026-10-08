import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { clienteService, type ClienteDetalle, type CronogramaEntry, type HistorialEntry } from '@/services/cliente.service'
import { prestamoService } from '@/services/prestamo.service'
import { formatDate } from '@/utils/format'
import { useUnsaved } from '@/contexts/UnsavedContext'

type Tab = 'info' | 'cronograma' | 'historial'

export default function ClienteDetailPage() {
  const { setDirty } = useUnsaved()
  const { id } = useParams()
  const navigate = useNavigate()
  const [cliente, setCliente] = useState<ClienteDetalle | null>(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<Tab>('info')
  const [cronograma, setCronograma] = useState<CronogramaEntry[]>([])
  const [historial, setHistorial] = useState<HistorialEntry[]>([])
  const [tabLoading, setTabLoading] = useState(false)
  const [togglingCuota, setTogglingCuota] = useState<number | null>(null)

  const handleToggleCuota = async (cronogramaId: number, prestamoId: number) => {
    if (togglingCuota !== null) return
    setTogglingCuota(cronogramaId)
    try {
      const res = await prestamoService.toggleCronogramaEstado(prestamoId, cronogramaId)
      if (res.success) {
        setDirty()
        setCronograma((prev) => prev.map((c) => c.id === cronogramaId ? { ...c, estado: res.data?.estado ?? c.estado } : c))
      }
    } catch {
      // ignore
    } finally {
      setTogglingCuota(null)
    }
  }

  useEffect(() => {
    if (!id) return
    clienteService.getById(Number(id)).then((res) => {
      if (res.success && res.data) setCliente(res.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [id])

  useEffect(() => {
    if (!id || !cliente) return
    if (tab === 'cronograma' && cronograma.length === 0) {
      setTabLoading(true)
      clienteService.getCronograma(Number(id)).then((res) => {
        if (res.success && res.data?.items) setCronograma(res.data.items)
        setTabLoading(false)
      }).catch(() => setTabLoading(false))
    }
    if (tab === 'historial' && historial.length === 0) {
      setTabLoading(true)
      clienteService.getHistorial(Number(id)).then((res) => {
        if (res.success && res.data?.items) setHistorial(res.data.items)
        setTabLoading(false)
      }).catch(() => setTabLoading(false))
    }
  }, [tab, id, cliente])

  const tabs: { key: Tab; label: string }[] = [
    { key: 'info', label: 'Información' },
    { key: 'cronograma', label: 'Cronograma' },
    { key: 'historial', label: 'Historial' },
  ]

  if (loading) return <div className="p-6 text-center text-surface-500">Cargando...</div>
  if (!cliente) return <div className="p-6 text-center text-red-500">Cliente no encontrado.</div>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button onClick={() => navigate('/clientes')} className="mb-4 text-sm text-primary-600 hover:underline">&larr; Volver a Clientes</button>

      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-surface-800">{cliente.nombre}</h1>
        <span className={`rounded-full px-3 py-1 text-xs font-medium ${
          cliente.estado === 'ACTIVO' ? 'bg-green-100 text-green-700' : 'bg-surface-100 text-surface-600'
        }`}>{cliente.estado}</span>
      </div>

      <div className="mb-4 border-b border-surface-200">
        <div className="flex gap-4">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`border-b-2 pb-2 text-sm font-medium ${
                tab === t.key ? 'border-primary-600 text-primary-600' : 'border-transparent text-surface-500 hover:text-surface-700'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {tab === 'info' && (
        <div className="grid gap-6 md:grid-cols-2">
          <div className="card p-4">
            <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Información Personal</h3>
            <div className="space-y-2 text-sm">
              <p><span className="text-surface-500">Cédula:</span> {cliente.cedula}</p>
              <p><span className="text-surface-500">Placa:</span> {cliente.placa}</p>
              <p><span className="text-surface-500">Teléfono:</span> {cliente.telefono || '-'}</p>
              <p><span className="text-surface-500">Dirección:</span> {cliente.direccion || '-'}</p>
              <p><span className="text-surface-500">Correo:</span> {cliente.correo || '-'}</p>
            </div>
          </div>

          {cliente.prestamo && (
            <div className="card p-4">
              <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Información Financiera</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-surface-500">Capital Inicial:</span> ${Number(cliente.prestamo.capital_inicial).toLocaleString('es-CO')}</p>
                <p><span className="text-surface-500">Saldo Actual:</span> ${Number(cliente.prestamo.saldo_actual).toLocaleString('es-CO')}</p>
                <p><span className="text-surface-500">Valor Cuota:</span> ${Number(cliente.prestamo.valor_cuota).toLocaleString('es-CO')}</p>
                <p><span className="text-surface-500">Tasa Interés:</span> {cliente.prestamo.tasa_interes}%</p>
                <p><span className="text-surface-500">Próximo Pago:</span> {formatDate(cliente.prestamo.fecha_proximo_pago)}</p>
                <p><span className="text-surface-500">Estado:</span> {cliente.prestamo.estado}</p>
              </div>
            </div>
          )}

          <div className="mt-4 flex gap-3">
            <button onClick={() => navigate(`/clientes/${id}/editar`)} className="btn-warning">Editar</button>
          </div>

          {cliente.observaciones && (
            <div className="card mt-6 p-4">
              <h3 className="mb-2 text-sm font-semibold text-surface-500 uppercase">Observaciones</h3>
              <p className="text-sm text-surface-700">{cliente.observaciones}</p>
            </div>
          )}
        </div>
      )}

      {tab === 'cronograma' && (
        <div className="card p-4">
          {tabLoading ? (
            <div className="text-center text-surface-500">Cargando...</div>
          ) : cronograma.length === 0 ? (
            <div className="text-center text-surface-500">Sin cronograma disponible.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-surface-500">
                    <th className="pb-2 pr-4">#</th>
                    <th className="pb-2 pr-4">Fecha</th>
                    <th className="pb-2 pr-4 text-right">Capital</th>
                    <th className="pb-2 pr-4 text-right">Interés</th>
                    <th className="pb-2 pr-4 text-right">Valor</th>
                    <th className="pb-2 pr-4 text-right">Saldo</th>
                    <th className="pb-2">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {cronograma.map((c) => (
                    <tr key={c.id} className="border-b last:border-0 hover:bg-surface-50">
                      <td className="py-2 pr-4">{c.numero_cuota}</td>
                      <td className="py-2 pr-4">{formatDate(c.fecha_estimada)}</td>
                      <td className="py-2 pr-4 text-right">${Number(c.capital_estimado).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-4 text-right">${Number(c.interes_estimado).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-4 text-right">${Number(c.valor_estimado).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-4 text-right">${Number(c.saldo_estimado).toLocaleString('es-CO')}</td>
                      <td className="py-2">
                        <div className="flex items-center gap-2">
                          <span className={`rounded px-2 py-0.5 text-xs ${
                            c.estado === 'PAGADO' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                          }`}>{c.estado}</span>
                          <button onClick={() => handleToggleCuota(c.id, c.prestamo_id)} disabled={togglingCuota === c.id} className="text-xs text-primary-600 hover:underline disabled:opacity-50">
                            {togglingCuota === c.id ? '...' : c.estado === 'PENDIENTE' ? 'Pagar' : 'Pendiente'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {tab === 'historial' && (
        <div className="card p-4">
          {tabLoading ? (
            <div className="text-center text-surface-500">Cargando...</div>
          ) : historial.length === 0 ? (
            <div className="text-center text-surface-500">Sin historial disponible.</div>
          ) : (
            <div className="space-y-3">
              {historial.map((h) => (
                <div key={h.id} className="border-l-4 border-primary-300 bg-primary-50 p-3 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-primary-800">{h.accion}</span>
                    <span className="text-xs text-surface-400">{formatDate(h.created_at)}</span>
                  </div>
                  {h.descripcion && <p className="mt-1 text-surface-600">{h.descripcion}</p>}
                  {h.usuario && <p className="mt-1 text-xs text-surface-400">por: {h.usuario}</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
