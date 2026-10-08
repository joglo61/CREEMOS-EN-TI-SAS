import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { prestamoService, type PrestamoItem } from '@/services/prestamo.service'
import { formatDate } from '@/utils/format'
import { pagoService, type PagoItem } from '@/services/pago.service'
import { descargar } from '@/services/excel.service'
import type { CronogramaEntry } from '@/services/cliente.service'
import { useUnsaved } from '@/contexts/UnsavedContext'
import { useToast } from '@/contexts/ToastContext'

type Tab = 'info' | 'cronograma' | 'pagos'

export default function PrestamoDetailPage() {
  const { setDirty } = useUnsaved()
  const { addToast } = useToast()
  const { id } = useParams()
  const navigate = useNavigate()
  const [prestamo, setPrestamo] = useState<PrestamoItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<Tab>('info')
  const [cronograma, setCronograma] = useState<CronogramaEntry[]>([])
  const [pagos, setPagos] = useState<PagoItem[]>([])
  const [tabLoading, setTabLoading] = useState(false)
  const [updatingEstado, setUpdatingEstado] = useState(false)
  const [togglingCuota, setTogglingCuota] = useState<number | null>(null)
  const [anulando, setAnulando] = useState(false)

  useEffect(() => {
    if (!id) return
    prestamoService.getById(Number(id)).then((res) => {
      if (res.success && res.data) setPrestamo(res.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [id])

  useEffect(() => {
    if (!id) return
    if (tab === 'cronograma' && cronograma.length === 0) {
      setTabLoading(true)
      prestamoService.getCronograma(Number(id)).then((res) => {
        if (res.success && res.data?.items) setCronograma(res.data.items)
        setTabLoading(false)
      }).catch(() => setTabLoading(false))
    }
    if (tab === 'pagos' && pagos.length === 0) {
      setTabLoading(true)
      pagoService.list({ prestamo_id: Number(id), page_size: 200 }).then((res) => {
        if (res.success && res.data?.items) setPagos(res.data.items)
        setTabLoading(false)
      }).catch(() => setTabLoading(false))
    }
  }, [tab, id])

  const handleToggleCuota = async (cronogramaId: number) => {
    if (!id || togglingCuota !== null) return
    setTogglingCuota(cronogramaId)
    try {
      const res = await prestamoService.toggleCronogramaEstado(Number(id), cronogramaId)
      if (res.success) {
        setDirty()
        setCronograma((prev) => prev.map((c) => c.id === cronogramaId ? { ...c, estado: res.data?.estado ?? c.estado } : c))
        addToast('success', `Cuota marcada como ${res.data?.estado}`)
      }
    } catch {
      addToast('error', 'Error al cambiar estado de la cuota')
    } finally {
      setTogglingCuota(null)
    }
  }

  const handleActualizarEstado = async () => {
    if (!id || updatingEstado) return
    setUpdatingEstado(true)
    try {
      const res = await prestamoService.actualizarEstado(Number(id))
      if (res.success) {
        setDirty()
        const nuevoEstado = res.data?.estado
        const reload = await prestamoService.getById(Number(id))
        if (reload.success && reload.data) setPrestamo(reload.data)
        addToast('success', `Estado actualizado a: ${nuevoEstado ?? 'desconocido'}`)
      } else {
        addToast('error', res.message ?? 'Error al actualizar estado.')
      }
    } catch {
      addToast('error', 'Error de red al actualizar estado.')
    } finally {
      setUpdatingEstado(false)
    }
  }

  const handleAnular = async () => {
    if (!id || anulando) return
    if (!window.confirm('¿Está seguro de anular este préstamo? Las cuotas pendientes también se cancelarán.')) return
    setAnulando(true)
    try {
      const res = await prestamoService.anular(Number(id))
      if (res.success) {
        setDirty()
        setPrestamo(prev => prev ? { ...prev, estado: 'CANCELADO' } : prev)
        addToast('success', res.message ?? 'Préstamo anulado.')
      } else {
        addToast('error', res.message ?? 'Error al anular.')
      }
    } catch {
      addToast('error', 'Error al anular el préstamo.')
    } finally {
      setAnulando(false)
    }
  }

  const estadoClass = (e: string) => {
    switch (e) {
      case 'ACTIVO': return 'bg-green-100 text-green-700'
      case 'MORA': return 'bg-red-100 text-red-700'
      case 'PAGADO': return 'bg-primary-100 text-primary-700'
      case 'CANCELADO': return 'bg-surface-200 text-surface-600'
      default: return 'bg-surface-100 text-surface-500'
    }
  }

  if (loading) return <div className="p-6 text-center text-surface-500">Cargando...</div>
  if (!prestamo) return <div className="p-6 text-center text-red-500">Préstamo no encontrado.</div>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button onClick={() => navigate('/prestamos')} className="mb-4 text-sm text-primary-600 hover:underline">&larr; Volver a Préstamos</button>

      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-surface-800">Préstamo #{prestamo.id}</h1>
        <span className={`rounded-full px-3 py-1 text-xs font-medium ${estadoClass(prestamo.estado)}`}>{prestamo.estado}</span>
      </div>

      <div className="mb-4 border-b border-surface-200">
        <div className="flex gap-4">
          {(['info', 'cronograma', 'pagos'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`border-b-2 pb-2 text-sm font-medium capitalize ${
                tab === t ? 'border-primary-600 text-primary-600' : 'border-transparent text-surface-500'
              }`}
            >
              {t === 'info' ? 'Información' : t === 'cronograma' ? 'Cronograma' : 'Pagos'}
            </button>
          ))}
        </div>
      </div>

      {tab === 'info' && (
        <div>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-4">
              <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Datos del Préstamo</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-surface-500">Cliente:</span> <span className="font-medium text-primary-600">{prestamo.cliente_nombre}</span></p>
                <p><span className="text-surface-500">Capital Inicial:</span> ${Number(prestamo.capital_inicial).toLocaleString('es-CO')}</p>
                <p><span className="text-surface-500">Saldo Actual:</span> <span className="font-bold">${Number(prestamo.saldo_actual).toLocaleString('es-CO')}</span></p>
                <p><span className="text-surface-500">Valor Cuota:</span> ${Number(prestamo.valor_cuota).toLocaleString('es-CO')}</p>
                <p><span className="text-surface-500">Tasa Interés:</span> {prestamo.tasa_interes}%</p>
              </div>
            </div>
            <div className="card p-4">
              <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Fechas</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-surface-500">Inicio:</span> {formatDate(prestamo.fecha_inicio)}</p>
                <p><span className="text-surface-500">Primer Pago:</span> {formatDate(prestamo.fecha_primer_pago)}</p>
                <p><span className="text-surface-500">Próximo Pago:</span> {formatDate(prestamo.fecha_proximo_pago)}</p>
              </div>
            </div>
          </div>
          <div className="mt-4 flex gap-3">
            <button onClick={() => navigate(`/prestamos/${id}/pagar`)} className="btn-success">
              Registrar Pago
            </button>
            <button onClick={handleActualizarEstado} disabled={updatingEstado} className="btn-primary">
              {updatingEstado ? 'Actualizando...' : 'Actualizar Estado'}
            </button>
            {prestamo.estado !== 'CANCELADO' && prestamo.estado !== 'PAGADO' && (
              <button onClick={handleAnular} disabled={anulando} className="btn-danger">
                {anulando ? 'Anulando...' : 'Anular Préstamo'}
              </button>
            )}
          </div>
        </div>
      )}

      {tab === 'cronograma' && (
        <div className="card p-4">
          {tabLoading ? <div className="text-center text-surface-500">Cargando...</div>
          : cronograma.length === 0 ? <div className="text-center text-surface-500">Sin cronograma.</div>
          : (
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
                          <span className={`rounded px-2 py-0.5 text-xs ${c.estado === 'PAGADO' ? 'bg-green-100 text-green-700' : c.estado === 'CANCELADO' ? 'bg-surface-200 text-surface-600' : 'bg-yellow-100 text-yellow-700'}`}>{c.estado}</span>
                          {c.estado === 'PENDIENTE' && (
                            <button onClick={() => handleToggleCuota(c.id)} disabled={togglingCuota === c.id} className="text-xs text-primary-600 hover:underline disabled:opacity-50">
                              {togglingCuota === c.id ? '...' : 'Pagar'}
                            </button>
                          )}
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

      {tab === 'pagos' && (
        <div className="card p-4">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-surface-500 uppercase">Historial de Pagos</h3>
            <div className="flex gap-2">
              <button
                onClick={() => descargar(`/prestamos/${id}/historial/excel`, `historial_prestamo_${id}.xlsx`).catch(() => alert('Error al exportar.'))}
                className="btn-secondary btn-xs"
              >
                Exportar historial
              </button>
              <button onClick={() => navigate(`/prestamos/${id}/pagar`)} className="btn-success btn-xs">
                + Nuevo Pago
              </button>
            </div>
          </div>
          {tabLoading ? <div className="text-center text-surface-500">Cargando...</div>
          : pagos.length === 0 ? <div className="text-center text-surface-500">Sin pagos registrados.</div>
          : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-surface-500">
                    <th className="pb-2 pr-3">Factura</th>
                    <th className="pb-2 pr-3">Fecha</th>
                    <th className="pb-2 pr-3 text-right">Valor</th>
                    <th className="pb-2 pr-3 text-right">Interés</th>
                    <th className="pb-2 pr-3 text-right">Capital</th>
                    <th className="pb-2 pr-3 text-right">Saldo Anterior</th>
                    <th className="pb-2 pr-3 text-right">Saldo Nuevo</th>
                    <th className="pb-2 pr-3">Días</th>
                    <th className="pb-2 pr-3">Usuario</th>
                    <th className="pb-2">Observaciones</th>
                  </tr>
                </thead>
                <tbody>
                  {pagos.map((p) => (
                    <tr key={p.id} className="border-b last:border-0 hover:bg-surface-50">
                      <td className="py-2 pr-3 font-mono text-xs">{p.numero_factura}</td>
                      <td className="py-2 pr-3">{formatDate(p.fecha_pago)}</td>
                      <td className="py-2 pr-3 text-right font-medium">${Number(p.valor_pagado).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-3 text-right">${(Number(p.intereses) + Number(p.intereses_mora || 0)).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-3 text-right">${Number(p.capital).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-3 text-right">${Number(p.saldo_anterior).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-3 text-right">${Number(p.saldo_nuevo).toLocaleString('es-CO')}</td>
                      <td className="py-2 pr-3">{p.dias_calculados}</td>
                      <td className="py-2 pr-3 text-xs text-surface-500">{p.usuario_nombre}</td>
                      <td className="py-2 text-xs text-surface-500">{p.observaciones}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
