import { useState, useEffect } from 'react'
import { excelService, type ExcelVersion, type ExcelEstado } from '@/services/excel.service'
import { formatDate } from '@/utils/format'

export default function ExcelManagementPage() {
  const [estado, setEstado] = useState<ExcelEstado | null>(null)
  const [versiones, setVersiones] = useState<ExcelVersion[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [removing, setRemoving] = useState<string | null>(null)
  const [exporting, setExporting] = useState(false)
  const [updating, setUpdating] = useState(false)
  const [restoring, setRestoring] = useState<number | null>(null)
  const load = () => {
    setLoading(true)
    Promise.all([
      excelService.getEstado(),
      excelService.getVersiones(),
    ]).then(([e, v]) => {
      if (e.success && e.data) setEstado(e.data)
      if (v.success && v.data) setVersiones(v.data.items)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleUpload = async (tipo: 'cartera_creemos') => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.xlsx,.xls'
    input.onchange = async () => {
      const file = input.files?.[0]
      if (!file) return
      setUploading(true)
      try {
        const res = await excelService.upload(tipo, file)
        if (res.success) load()
      } catch (err: any) {
        const d = err?.response?.data?.detail
        alert(typeof d === 'string' ? d : JSON.stringify(d) || 'Error al subir archivo.')
      } finally {
        setUploading(false)
      }
    }
    input.click()
  }

  const handleRemove = async (key: string, label: string) => {
    if (!confirm(`¿Eliminar el archivo "${label}" del sistema?`)) return
    setRemoving(key)
    try {
      const res = await excelService.eliminarActivo(key)
      if (res.success) load()
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Error al eliminar.')
    } finally {
      setRemoving(null)
    }
  }

  const handleExportar = async () => {
    setExporting(true)
    try {
      await excelService.exportarTodo()
    } catch (err: any) {
      alert(err?.response?.data?.detail || err?.message || 'Error al exportar.')
    } finally {
      setExporting(false)
    }
  }

  const handleActualizarExcel = async () => {
    if (!confirm('¿Actualizar Creemos.xlsx? Se escribirán los pagos del sistema en el Excel (marcando en color los que pagaron), se creará el bloque del mes si falta, y se re-sincronizará. Cierra el archivo en Excel antes de continuar.')) return
    setUpdating(true)
    try {
      const res = await excelService.actualizarExcelCartera()
      if (res.success && res.data) {
        const d = res.data
        const partes = [`✅ ${res.message || 'Actualizado.'}`]
        if (d.bloque_nuevo) partes.push(`Bloque nuevo: ${d.bloque_nuevo.label} (${d.bloque_nuevo.filas} filas, ${d.bloque_nuevo.altas} altas)`)
        partes.push(`Pagos escritos al bloque: ${d.pagos_excel.escritos_bloque}, a hojas: ${d.pagos_excel.escritos_hoja}`)
        partes.push(`Sistema: ${d.importacion.clientes} clientes, ${d.importacion.prestamos} préstamos, ${d.importacion.pagos} pagos`)
        alert(partes.join('\n'))
        load()
      }
    } catch (err: any) {
      const d = err?.response?.data?.detail
      alert(typeof d === 'string' ? d : JSON.stringify(d) || 'Error al actualizar.')
    } finally {
      setUpdating(false)
    }
  }

  const handleRestaurar = async (archivoId: number) => {
    if (!confirm('¿Restaurar esta versión? Se creará un respaldo de la actual.')) return
    setRestoring(archivoId)
    try {
      const res = await excelService.restaurar(archivoId)
      if (res.success) load()
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Error al restaurar.')
    } finally {
      setRestoring(null)
    }
  }

  if (loading) return <div className="p-6 text-center text-surface-500">Cargando...</div>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="mb-6 text-2xl font-bold text-surface-800">Administración de Archivos Excel</h1>

      <div className="mb-6 grid gap-4 md:grid-cols-2">
        {([
          { key: 'cartera_creemos', label: 'CREEMOS (Cartera)' },
        ] as const).map(({ key, label }) => {
          const st = estado?.[key]
          return (
            <div key={key} className="card p-4">
              <h3 className="mb-2 text-sm font-semibold text-surface-500 uppercase">{label}</h3>
              {st?.activo ? (
                <div className="space-y-1 text-sm">
                  <p><span className="text-surface-500">Archivo:</span> {st.nombre}</p>
                  <p><span className="text-surface-500">Tamaño:</span> {st.tamano ? `${(st.tamano / 1024).toFixed(1)} KB` : '-'}</p>
                  <p><span className="text-surface-500">Modificado:</span> {formatDate(st.fecha)}</p>
                </div>
              ) : (
                <p className="text-sm text-surface-400">Sin archivo activo.</p>
              )}
              <div className="mt-3 flex flex-wrap gap-2">
                <button
                  onClick={() => handleUpload(key)}
                  disabled={uploading}
                  className="btn-primary btn-sm"
                >
                  {uploading ? 'Subiendo...' : 'Subir Archivo'}
                </button>
                <button
                  onClick={handleActualizarExcel}
                  disabled={updating || !st?.activo}
                  className="btn-success btn-sm"
                  title="Escribe los pagos del sistema en el Excel (con color), crea el bloque del mes si falta y re-sincroniza"
                >
                  {updating ? 'Actualizando...' : 'Actualizar Excel'}
                </button>
                {st?.activo && (
                  <button
                    onClick={() => excelService.descargarCartera().catch(() => alert('Error al descargar.'))}
                    className="btn-secondary btn-sm"
                  >
                    Descargar
                  </button>
                )}
                {st?.activo && (
                  <button
                    onClick={() => handleRemove(key, label)}
                    disabled={removing === key}
                    className="btn-danger btn-sm"
                  >
                    {removing === key ? '...' : 'Quitar'}
                  </button>
                )}
              </div>
            </div>
          )
        })}

        <div className="card p-4">
          <h3 className="mb-2 text-sm font-semibold text-surface-500 uppercase">Exportar Todo</h3>
          <p className="mb-3 text-sm text-surface-400">Descarga un Excel completo con clientes, préstamos, pagos y facturas.</p>
          <button
            onClick={handleExportar}
            disabled={exporting}
            className="btn-success btn-sm"
          >
            {exporting ? 'Exportando...' : 'Descargar Respaldo Excel'}
          </button>
        </div>
      </div>

      <div className="card p-4">
        <h3 className="mb-3 text-sm font-semibold text-surface-500 uppercase">Historial de Versiones</h3>
        {versiones.length === 0 ? (
          <p className="text-sm text-surface-400">Sin versiones registradas.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-surface-500">
                  <th className="pb-2 pr-3">Tipo</th>
                  <th className="pb-2 pr-3">Versión</th>
                  <th className="pb-2 pr-3">Nombre</th>
                  <th className="pb-2 pr-3">Estado</th>
                  <th className="pb-2 pr-3">Fecha</th>
                  <th className="pb-2 pr-3">Usuario</th>
                  <th className="pb-2">Acción</th>
                </tr>
              </thead>
              <tbody>
                {versiones.map((v) => (
                  <tr key={v.id} className="border-b last:border-0 hover:bg-surface-50">
                    <td className="py-2 pr-3 capitalize">{v.tipo}</td>
                    <td className="py-2 pr-3">v{v.version}</td>
                    <td className="py-2 pr-3 text-xs">{v.nombre}</td>
                    <td className="py-2 pr-3">
                      {v.activo ? (
                        <span className="rounded bg-green-100 px-2 py-0.5 text-xs text-green-700">Activo</span>
                      ) : (
                        <span className="rounded bg-surface-100 px-2 py-0.5 text-xs text-surface-500">Histórico</span>
                      )}
                    </td>
                    <td className="py-2 pr-3 text-xs">{formatDate(v.fecha)}</td>
                    <td className="py-2 pr-3 text-xs text-surface-500">{v.usuario}</td>
                    <td className="py-2">
                      {!v.activo && (
                        <button
                          onClick={() => handleRestaurar(v.id)}
                          disabled={restoring === v.id}
                          className="btn-warning btn-xs"
                        >
                          {restoring === v.id ? '...' : 'Restaurar'}
                        </button>
                      )}
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
