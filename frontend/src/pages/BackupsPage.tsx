import { useState, useEffect } from 'react'
import api from '@/services/api'
import type { ApiResponse } from '@/types/auth'
import { formatDate } from '@/utils/format'

interface BackupItem {
  id: number
  tipo: string
  archivo: string
  tamano: number | null
  fecha: string | null
  usuario: string
}

export default function BackupsPage() {
  const [items, setItems] = useState<BackupItem[]>([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [restoring, setRestoring] = useState<number | null>(null)
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    api.get<ApiResponse<{items: BackupItem[]}>>('/backups').then((res) => {
      if (res.data.success && res.data.data) setItems(res.data.data.items)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleCrear = async (tipo: string) => {
    setCreating(true)
    setError('')
    try {
      const res = await api.post<ApiResponse>(`/backups/crear?tipo=${tipo}`)
      if (res.data.success) { load() }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Error al crear backup.')
    } finally {
      setCreating(false)
    }
  }

  const handleRestaurar = async (id: number) => {
    if (!confirm('¿Restaurar este backup? Se creará un respaldo automático del estado actual.')) return
    setRestoring(id)
    setError('')
    try {
      const res = await api.post<ApiResponse>(`/backups/restaurar/${id}`)
      if (res.data.success) { alert('Backup restaurado. Se recomienda reiniciar la aplicación.') }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Error al restaurar.')
    } finally {
      setRestoring(null)
    }
  }

  const formatSize = (bytes: number | null) => {
    if (!bytes) return '-'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const tipoColor = (tipo: string) => {
    switch (tipo) {
      case 'base_datos': return 'bg-blue-100 text-blue-700'
      case 'config': return 'bg-purple-100 text-purple-700'
      default: return 'bg-gray-100 text-gray-600'
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="mb-6 text-2xl font-bold text-gray-800">Backups</h1>

      {error && <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <button onClick={() => handleCrear('completo')} disabled={creating} className="rounded-lg bg-blue-600 p-4 text-white shadow hover:bg-blue-700 disabled:opacity-50 text-left">
          <p className="text-sm font-medium uppercase opacity-80">Completo</p>
          <p className="mt-1 text-lg font-bold">{creating ? 'Creando...' : 'Crear Backup'}</p>
          <p className="mt-1 text-xs opacity-70">BD + Configuración</p>
        </button>
        <button onClick={() => handleCrear('base_datos')} disabled={creating} className="rounded-lg bg-green-600 p-4 text-white shadow hover:bg-green-700 disabled:opacity-50 text-left">
          <p className="text-sm font-medium uppercase opacity-80">Base de Datos</p>
          <p className="mt-1 text-lg font-bold">{creating ? 'Creando...' : 'Backup BD'}</p>
          <p className="mt-1 text-xs opacity-70">Solo SQLite</p>
        </button>
        <button onClick={() => handleCrear('config')} disabled={creating} className="rounded-lg bg-purple-600 p-4 text-white shadow hover:bg-purple-700 disabled:opacity-50 text-left">
          <p className="text-sm font-medium uppercase opacity-80">Configuración</p>
          <p className="mt-1 text-lg font-bold">{creating ? 'Creando...' : 'Backup Config'}</p>
          <p className="mt-1 text-xs opacity-70">Parámetros del sistema</p>
        </button>
      </div>

      <div className="rounded-lg bg-white p-4 shadow">
        <h3 className="mb-3 text-sm font-semibold text-gray-500 uppercase">Historial de Backups</h3>
        {loading ? (
          <p className="text-sm text-gray-400">Cargando...</p>
        ) : items.length === 0 ? (
          <p className="text-sm text-gray-400">Sin backups registrados.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-gray-500">
                  <th className="pb-2 pr-3">Tipo</th>
                  <th className="pb-2 pr-3">Archivo</th>
                  <th className="pb-2 pr-3 text-right">Tamaño</th>
                  <th className="pb-2 pr-3">Fecha</th>
                  <th className="pb-2 pr-3">Usuario</th>
                  <th className="pb-2">Acción</th>
                </tr>
              </thead>
              <tbody>
                {items.map((b) => (
                  <tr key={b.id} className="border-b last:border-0 hover:bg-gray-50">
                    <td className="py-2 pr-3">
                      <span className={`rounded px-2 py-0.5 text-xs ${tipoColor(b.tipo)}`}>{b.tipo}</span>
                    </td>
                    <td className="py-2 pr-3 font-mono text-xs">{b.archivo}</td>
                    <td className="py-2 pr-3 text-right">{formatSize(b.tamano)}</td>
                    <td className="py-2 pr-3 text-xs">{formatDate(b.fecha)}</td>
                    <td className="py-2 pr-3 text-xs text-gray-500">{b.usuario}</td>
                    <td className="py-2">
                      <button
                        onClick={() => handleRestaurar(b.id)}
                        disabled={restoring === b.id}
                        className="rounded bg-yellow-500 px-2 py-1 text-xs text-white hover:bg-yellow-600 disabled:opacity-50"
                      >
                        {restoring === b.id ? '...' : 'Restaurar'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
