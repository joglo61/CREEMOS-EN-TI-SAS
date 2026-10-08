import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { prestamoService, type PrestamoItem } from '@/services/prestamo.service'
import { formatDate } from '@/utils/format'

export default function PrestamosListPage() {
  const navigate = useNavigate()
  const [items, setItems] = useState<PrestamoItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [estado, setEstado] = useState('')
  const [page, setPage] = useState(1)
  const pageSize = 25

  useEffect(() => {
    setLoading(true)
    prestamoService.list({ search, estado, page, page_size: pageSize }).then((res) => {
      if (res.success && res.data) {
        setItems(res.data.items)
        setTotal(res.data.total)
      }
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [search, estado, page])

  const totalPages = Math.ceil(total / pageSize)

  const estadoClass = (e: string) => {
    switch (e) {
      case 'ACTIVO': return 'badge-green'
      case 'MORA': return 'badge-red'
      case 'PAGADO': return 'badge-blue'
      case 'CANCELADO': return 'badge-gray'
      default: return 'badge-gray'
    }
  }

  return (
    <div className="p-6 lg:p-8 animate-fade-in">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="page-title">Préstamos</h1>
          <p className="mt-1 text-sm text-surface-400">{total} préstamo(s)</p>
        </div>
        <button onClick={() => navigate('/prestamos/nuevo')} className="btn-primary">
          + Nuevo Préstamo
        </button>
      </div>

      <div className="mb-4 flex gap-2">
        <input
          type="text" placeholder="Buscar por placa..."
          value={search} onChange={(e) => { setSearch(e.target.value); setPage(1) }}
          className="input flex-1"
        />
        <select value={estado} onChange={(e) => { setEstado(e.target.value); setPage(1) }} className="select w-40">
          <option value="">Todos</option>
          <option value="ACTIVO">Activo</option>
          <option value="MORA">Mora</option>
          <option value="PAGADO">Pagado</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-primary-200 border-t-primary-600" />
        </div>
      ) : items.length === 0 ? (
        <div className="card p-12 text-center text-surface-400">Sin préstamos registrados.</div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Cliente</th>
                <th>Placa</th>
                <th className="text-right">Capital</th>
                <th className="text-right">Saldo</th>
                <th className="text-right">Cuota</th>
                <th>Próximo Pago</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {items.map((p) => (
                <tr key={p.id} className="cursor-pointer" onClick={() => navigate(`/prestamos/${p.id}`)}>
                  <td className="font-mono text-xs">{p.id}</td>
                  <td className="font-medium text-primary-600">{p.cliente_nombre}</td>
                  <td className="uppercase">{p.cliente_placa}</td>
                  <td className="text-right">${Number(p.capital_inicial).toLocaleString()}</td>
                  <td className="text-right font-medium">${Number(p.saldo_actual).toLocaleString()}</td>
                  <td className="text-right">${Number(p.valor_cuota).toLocaleString()}</td>
                  <td>{formatDate(p.fecha_proximo_pago)}</td>
                  <td><span className={`badge ${estadoClass(p.estado)}`}>{p.estado}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-center gap-2 text-sm">
          <button disabled={page <= 1} onClick={() => setPage(page - 1)} className="btn-secondary btn-sm">&larr; Anterior</button>
          <span className="text-surface-400">Página {page} de {totalPages}</span>
          <button disabled={page >= totalPages} onClick={() => setPage(page + 1)} className="btn-secondary btn-sm">Siguiente &rarr;</button>
        </div>
      )}
    </div>
  )
}
