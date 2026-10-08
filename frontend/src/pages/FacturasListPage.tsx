import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { facturaService, type FacturaItem } from '@/services/factura.service'
import { formatDate } from '@/utils/format'
import { useUnsaved } from '@/contexts/UnsavedContext'
import { useToast } from '@/contexts/ToastContext'

export default function FacturasListPage() {
  const { setDirty } = useUnsaved()
  const { addToast } = useToast()
  const navigate = useNavigate()
  const [items, setItems] = useState<FacturaItem[]>([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [deleting, setDeleting] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [estado, setEstado] = useState('')

  const load = () => {
    setLoading(true)
    facturaService.list({ page_size: 200, search, estado }).then((res) => {
      if (res.success && res.data) setItems(res.data.items)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [search, estado])

  const toggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id); else next.add(id)
      return next
    })
  }

  const toggleAll = () => {
    if (selected.size === items.length) setSelected(new Set())
    else setSelected(new Set(items.map((f) => f.id)))
  }

  const handleDelete = async () => {
    setDeleting(true)
    for (const id of selected) {
      try { await facturaService.delete(id); setDirty() } catch { /* skip */ }
    }
    setSelected(new Set())
    setDeleting(false)
    setConfirmOpen(false)
    addToast('success', `Facturas eliminadas: ${selected.size}`)
    load()
  }

  const handleDownloadPDF = async (id: number, numeroFactura: string) => {
    try {
      const res = await facturaService.descargarPDF(id)
      const url = window.URL.createObjectURL(new Blob([res]))
      const a = document.createElement('a')
      a.href = url
      a.download = `factura_${numeroFactura}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch {
      addToast('error', 'Error al descargar PDF')
    }
  }

  return (
    <div className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-surface-800">Facturas</h1>
        {selected.size > 0 && (
          <button onClick={() => setConfirmOpen(true)} disabled={deleting} className="btn-danger">
            {deleting ? 'Eliminando...' : `Eliminar (${selected.size})`}
          </button>
        )}
      </div>

      <div className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Buscar por cliente o número de factura..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500"
        />
        <select value={estado} onChange={(e) => setEstado(e.target.value)} className="rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500">
          <option value="">Todos</option>
          <option value="EMITIDA">Emitida</option>
          <option value="ANULADA">Anulada</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center text-surface-500">Cargando...</div>
      ) : items.length === 0 ? (
        <div className="text-center text-surface-500">Sin facturas registradas.</div>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-surface-50 text-left text-surface-500">
                <th className="px-4 py-3">
                  <input type="checkbox" checked={selected.size === items.length && items.length > 0} onChange={toggleAll} className="cursor-pointer" />
                </th>
                <th className="px-4 py-3"># Factura</th>
                <th className="px-4 py-3">Cliente</th>
                <th className="px-4 py-3 text-right">Valor</th>
                <th className="px-4 py-3">Fecha</th>
                <th className="px-4 py-3">Estado</th>
                <th className="px-4 py-3">PDF</th>
              </tr>
            </thead>
            <tbody>
              {items.map((f) => (
                <tr key={f.id} className="border-b hover:bg-surface-50">
                  <td className="px-4 py-3" onClick={(e) => e.stopPropagation()}>
                    <input type="checkbox" checked={selected.has(f.id)} onChange={() => toggle(f.id)} className="cursor-pointer" />
                  </td>
                  <td className="px-4 py-3 font-mono text-xs font-medium cursor-pointer" onClick={() => navigate(`/facturas/${f.id}`)}>{f.numero_factura}</td>
                  <td className="px-4 py-3 cursor-pointer" onClick={() => navigate(`/facturas/${f.id}`)}>{f.cliente_nombre}</td>
                  <td className="px-4 py-3 text-right cursor-pointer" onClick={() => navigate(`/facturas/${f.id}`)}>${Number(f.pago_valor).toLocaleString('es-CO')}</td>
                  <td className="px-4 py-3 cursor-pointer" onClick={() => navigate(`/facturas/${f.id}`)}>{formatDate(f.fecha)}</td>
                  <td className="px-4 py-3 cursor-pointer" onClick={() => navigate(`/facturas/${f.id}`)}>
                    <span className={`rounded px-2 py-0.5 text-xs ${f.estado === 'EMITIDA' ? 'bg-primary-100 text-primary-700' : 'bg-surface-100 text-surface-600'}`}>{f.estado}</span>
                  </td>
                  <td className="px-4 py-3">
                    {f.ruta_pdf ? (
                      <button onClick={() => handleDownloadPDF(f.id, f.numero_factura)} className="text-xs text-primary-600 hover:underline">
                        Descargar
                      </button>
                    ) : (
                      <span className="text-xs text-surface-400">Pendiente</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {confirmOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setConfirmOpen(false)}>
          <div className="rounded-xl bg-white p-6 shadow-premium" onClick={(e) => e.stopPropagation()}>
            <h3 className="mb-2 text-lg font-semibold text-surface-800">Confirmar eliminación</h3>
            <p className="mb-1 text-sm text-surface-600">Se eliminarán <strong>{selected.size}</strong> factura(s) seleccionada(s).</p>
            <p className="mb-4 text-sm text-surface-500">Esta acción no se puede deshacer.</p>
            <div className="flex justify-end gap-3">
              <button onClick={() => setConfirmOpen(false)} className="rounded-md border px-4 py-2 text-sm text-surface-700 hover:bg-surface-50">Cancelar</button>
              <button onClick={handleDelete} disabled={deleting} className="btn-danger">
                {deleting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
