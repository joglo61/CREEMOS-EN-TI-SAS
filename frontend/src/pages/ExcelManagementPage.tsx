import { useState } from 'react'
import { excelService } from '@/services/excel.service'

// El sistema es la fuente de verdad: el Excel ya no se sube ni se sincroniza.
// Solo queda descargar un respaldo completo en Excel.
export default function ExcelManagementPage() {
  const [exporting, setExporting] = useState(false)

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

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="page-title mb-6">Respaldo en Excel</h1>
      <div className="card p-6">
        <p className="mb-4 text-sm text-surface-600">
          Descarga un Excel con todos los clientes, préstamos, pagos y facturas del sistema.
          Para el reporte mensual de cartera use <strong>Reportes → Cartera mensual</strong>.
        </p>
        <button onClick={handleExportar} disabled={exporting} className="btn-success">
          {exporting ? 'Exportando...' : 'Descargar respaldo Excel'}
        </button>
      </div>
    </div>
  )
}
