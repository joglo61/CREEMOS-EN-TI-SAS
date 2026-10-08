import { useState, useEffect } from 'react'
import { syncService, type SyncHistorialItem, type SyncResult } from '@/services/sync.service'
import { formatDate } from '@/utils/format'
import { useUnsaved } from '@/contexts/UnsavedContext'

export default function SynchronizationPage() {
  const { markClean } = useUnsaved()
  const [historial, setHistorial] = useState<SyncHistorialItem[]>([])
  const [loading, setLoading] = useState(true)
  const [syncing, setSyncing] = useState<string | null>(null)
  const [result, setResult] = useState<{ tipo: string; data: SyncResult } | null>(null)

  const load = () => {
    setLoading(true)
    syncService.getHistorial().then((res) => {
      if (res.success && res.data) setHistorial(res.data.items)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleSync = async (tipo: 'clientes' | 'financiero' | 'cartera') => {
    setSyncing(tipo)
    setResult(null)
    try {
      const res = await syncService.sincronizar(tipo)
      if (res.success) {
        setResult({ tipo, data: res.data! })
        load()
      }
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Error de sincronización.')
    } finally {
      setSyncing(null)
    }
  }

  const handleExport = async () => {
    setSyncing('export')
    try {
      const res = await syncService.exportarPagos(30)
      if (res.success) {
        alert('Pagos exportados a Excel correctamente.')
        load()
      }
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Error al exportar.')
    } finally {
      setSyncing(null)
    }
  }

  const handleGuardar = async () => {
    setSyncing('guardar')
    try {
      const res = await syncService.guardarEnExcel()
      if (res.success) {
        markClean()
        alert('Datos guardados en Excel correctamente.')
        load()
      }
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Error al guardar en Excel.')
    } finally {
      setSyncing(null)
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="mb-6 text-2xl font-bold text-surface-800">Sincronización</h1>

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <button
          onClick={() => handleSync('cartera')}
          disabled={syncing !== null}
          className="card-hover p-4 text-left disabled:opacity-50"
        >
          <h3 className="text-sm font-semibold text-surface-500 uppercase">Cartera</h3>
          <p className="mt-2 text-lg font-bold text-primary-600">
            {syncing === 'cartera' ? 'Sincronizando...' : 'Sincronizar'}
          </p>
          <p className="text-xs text-surface-400">Sincronizar CUENTAS JOGLO y POR COBRAR</p>
        </button>
        <button
          onClick={handleExport}
          disabled={syncing !== null}
          className="card-hover p-4 text-left disabled:opacity-50"
        >
          <h3 className="text-sm font-semibold text-surface-500 uppercase">Exportar Pagos</h3>
          <p className="mt-2 text-lg font-bold text-green-600">
            {syncing === 'export' ? 'Exportando...' : 'Exportar'}
          </p>
          <p className="text-xs text-surface-400">Exportar últimos 30 días a Excel</p>
        </button>
        <button
          onClick={handleGuardar}
          disabled={syncing !== null}
          className="card-hover p-4 text-left disabled:opacity-50"
        >
          <h3 className="text-sm font-semibold text-surface-500 uppercase">Guardar en Excel</h3>
          <p className="mt-2 text-lg font-bold text-purple-600">
            {syncing === 'guardar' ? 'Guardando...' : 'Guardar'}
          </p>
          <p className="text-xs text-surface-400">Sobrescribir datos en el archivo .xlsx</p>
        </button>
      </div>

      {result && (
        <div className="mb-6 rounded-lg bg-green-50 p-4 text-sm text-green-800">
          <p className="font-medium capitalize">Sincronización de {result.tipo} completada</p>
          {result.data.creados !== undefined && <p>Creados: {result.data.creados}</p>}
          {result.data.actualizados !== undefined && <p>Actualizados: {result.data.actualizados}</p>}
          {result.data.errores !== undefined && <p>Errores: {result.data.errores}</p>}
          {result.data.clientes !== undefined && <p>Clientes cartera.db: {result.data.clientes}</p>}
          {result.data.creditos !== undefined && <p>Créditos: {result.data.creditos}</p>}
          {result.data.pagos !== undefined && <p>Pagos cartera.db: {result.data.pagos}</p>}
          {result.data.snapshots !== undefined && <p>Snapshots: {result.data.snapshots}</p>}
          {result.data.importados && (
            <div className="mt-2 border-t border-green-200 pt-2">
              <p className="font-medium">Importados al sistema:</p>
              <p>Clientes: {result.data.importados.clientes}</p>
              <p>Préstamos: {result.data.importados.prestamos}</p>
              <p>Pagos: {result.data.importados.pagos}</p>
              <p>Eliminados previos: {result.data.importados.eliminados}</p>
            </div>
          )}
        </div>
      )}

      <div className="card p-4">
        <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Historial de Sincronización</h3>
        {loading ? (
          <p className="text-sm text-surface-400">Cargando...</p>
        ) : historial.length === 0 ? (
          <p className="text-sm text-surface-400">Sin actividad de sincronización.</p>
        ) : (
          <div className="space-y-2">
            {historial.map((h) => (
              <div key={h.id} className="border-l-4 border-primary-300 bg-primary-50 p-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-primary-800">{h.accion}</span>
                  <span className="text-xs text-surface-400">{formatDate(h.fecha)}</span>
                </div>
                {h.descripcion && <p className="mt-1 text-surface-600">{h.descripcion}</p>}
                <p className="mt-1 text-xs text-surface-400">por {h.usuario}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
