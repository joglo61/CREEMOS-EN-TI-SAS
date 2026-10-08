import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { facturaService, type FacturaItem } from '@/services/factura.service'
import { formatDate } from '@/utils/format'

export default function FacturaDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [factura, setFactura] = useState<FacturaItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [pdfReady, setPdfReady] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [blobUrl, setBlobUrl] = useState<string | null>(null)
  const iframeRef = useRef<HTMLIFrameElement>(null)

  useEffect(() => {
    if (!id) return
    facturaService.getById(Number(id)).then((res) => {
      if (res.success && res.data) {
        setFactura(res.data)
        if (res.data.ruta_pdf) loadPdf(Number(id))
      }
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [id])

  const loadPdf = async (facturaId: number) => {
    try {
      const blob = await facturaService.descargarPDF(facturaId)
      const url = URL.createObjectURL(blob)
      setBlobUrl(url)
      setPdfReady(true)
    } catch {
      setPdfReady(false)
    }
  }

  useEffect(() => {
    return () => { if (blobUrl) URL.revokeObjectURL(blobUrl) }
  }, [blobUrl])

  const handleGenerarPdf = async () => {
    if (!id) return
    setGenerating(true)
    try {
      const res = await facturaService.generarPdf(Number(id))
      if (res.success) {
        setFactura((prev) => prev ? { ...prev, ruta_pdf: res.data?.ruta_pdf ?? null } : prev)
        await loadPdf(Number(id))
      }
    } finally {
      setGenerating(false)
    }
  }

  if (loading) return <div className="p-6 text-center text-gray-500">Cargando...</div>
  if (!factura) return <div className="p-6 text-center text-red-500">Factura no encontrada.</div>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button onClick={() => navigate(-1)} className="mb-4 text-sm text-blue-600 hover:underline">&larr; Volver</button>

      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Recibo {factura.numero_factura}</h1>
          <p className="text-sm text-gray-500">{factura.cliente_nombre} - {formatDate(factura.fecha)}</p>
        </div>
        <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">{factura.estado}</span>
      </div>

      <div className="mb-6 flex gap-3">
        <button onClick={handleGenerarPdf} disabled={generating} className="rounded-md bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50">
          {generating ? 'Generando...' : pdfReady ? 'Volver a generar' : 'Generar PDF'}
        </button>
        {pdfReady && blobUrl && (
          <>
            <a href={blobUrl} download={`recibo_${factura.numero_factura}.pdf`} className="rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700">
              Abrir PDF
            </a>
            <button onClick={() => window.print()} className="rounded-md border px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
              Imprimir
            </button>
          </>
        )}
      </div>

      {pdfReady && blobUrl && (
        <div className="rounded-lg border bg-white p-2 shadow" style={{ height: '70vh' }}>
          <iframe ref={iframeRef} src={blobUrl} className="h-full w-full" title="Recibo PDF" />
        </div>
      )}
    </div>
  )
}
