import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { clienteService, type ClienteListado } from '@/services/cliente.service'
import { useToast } from '@/contexts/ToastContext'

export default function ClientesListPage() {
  const navigate = useNavigate()
  const { addToast } = useToast()
  const [clientes, setClientes] = useState<ClienteListado[]>([])
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [estado, setEstado] = useState('')
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [toggingId, setToggingId] = useState<number | null>(null)
  const pageSize = 25

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const res = await clienteService.list({ search, estado, page, page_size: pageSize })
      if (res.success && res.data) {
        setClientes(res.data.items)
        setTotal(res.data.total)
      }
    } catch {
      // ignore
    } finally {
      setLoading(false)
    }
  }, [search, estado, page])

  useEffect(() => { load() }, [load])

  useEffect(() => { setPage(1) }, [search, estado])

  const handleToggleEstado = async (id: number, nombre: string, estadoActual: string) => {
    if (toggingId !== null) return
    const accion = estadoActual === 'ACTIVO' ? 'archivar' : 'reactivar'
    if (!window.confirm(`¿Está seguro de ${accion} a "${nombre}"?`)) return
    setToggingId(id)
    try {
      const res = await clienteService.toggleEstado(id)
      if (res.success) {
        addToast('success', `Cliente ${res.data?.estado === 'ACTIVO' ? 'reactivado' : 'archivado'} correctamente.`)
        load()
      }
    } catch {
      addToast('error', 'Error al cambiar estado del cliente.')
    } finally {
      setToggingId(null)
    }
  }

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-surface-800">Clientes</h1>
        <button
          onClick={() => navigate('/clientes/nuevo')}
          className="btn-primary"
        >
          + Nuevo Cliente
        </button>
      </div>

      <div className="mb-4 flex gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Buscar por placa, nombre o cédula..."
          className="flex-1 rounded-md border border-surface-300 px-4 py-2 focus:border-primary-500 focus:outline-none"
        />
        <select value={estado} onChange={(e) => setEstado(e.target.value)} className="rounded-md border px-3 py-2 text-sm outline-none">
          <option value="">Todos</option>
          <option value="ACTIVO">Activos</option>
          <option value="INACTIVO">Inactivos</option>
        </select>
      </div>

      <div className="card overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b bg-surface-50 text-xs uppercase text-surface-600">
            <tr>
              <th className="px-4 py-3">Placa</th>
              <th className="px-4 py-3">Nombre</th>
              <th className="px-4 py-3">Teléfono</th>
              <th className="px-4 py-3">Saldo</th>
              <th className="px-4 py-3">Próximo Pago</th>
              <th className="px-4 py-3">Estado</th>
              <th className="px-4 py-3">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {loading ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-surface-500">Cargando...</td>
              </tr>
            ) : clientes.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-surface-500">No se encontraron clientes.</td>
              </tr>
            ) : (
              clientes.map((c) => (
                <tr key={c.id} className="hover:bg-surface-50">
                  <td className="px-4 py-3 font-medium">{c.placa}</td>
                  <td className="px-4 py-3">{c.nombre}</td>
                  <td className="px-4 py-3">{c.telefono || '-'}</td>
                  <td className="px-4 py-3">-</td>
                  <td className="px-4 py-3">-</td>
                  <td className="px-4 py-3">
                    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                      c.estado === 'ACTIVO' ? 'bg-green-100 text-green-700' : 'bg-surface-100 text-surface-600'
                    }`}>
                      {c.estado}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <button onClick={() => navigate(`/clientes/${c.id}`)} className="mr-2 text-primary-600 hover:underline">
                      Ver
                    </button>
                    <button onClick={() => navigate(`/clientes/${c.id}/editar`)} className="mr-2 text-yellow-600 hover:underline">
                      Editar
                    </button>
                    <button onClick={() => handleToggleEstado(c.id, c.nombre, c.estado)} disabled={toggingId === c.id} className="text-red-600 hover:underline disabled:opacity-50">
                      {toggingId === c.id ? '...' : c.estado === 'ACTIVO' ? 'Archivar' : 'Reactivar'}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-between text-sm text-surface-600">
          <span>{total} cliente(s)</span>
          <div className="flex gap-2">
            <button disabled={page <= 1} onClick={() => setPage(page - 1)} className="rounded border px-3 py-1 disabled:opacity-50">
              Anterior
            </button>
            <span className="px-2 py-1">Pág {page} de {totalPages}</span>
            <button disabled={page >= totalPages} onClick={() => setPage(page + 1)} className="rounded border px-3 py-1 disabled:opacity-50">
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
