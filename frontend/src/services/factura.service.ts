import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface FacturaItem {
  id: number
  numero_factura: string
  cliente_id: number
  pago_id: number
  fecha: string
  ruta_pdf: string | null
  estado: string
  created_at: string | null
  cliente_nombre: string
  pago_valor: string
}

export const facturaService = {
  async list(params: { page?: number; page_size?: number; search?: string; estado?: string }) {
    const res = await api.get<ApiResponse<{items: FacturaItem[]}>>('/facturas', { params })
    return res.data
  },

  async getById(id: number) {
    const res = await api.get<ApiResponse<FacturaItem>>(`/facturas/${id}`)
    return res.data
  },

  async generarPdf(id: number) {
    const res = await api.post<ApiResponse<{ruta_pdf: string}>>(`/facturas/${id}/generar-pdf`)
    return res.data
  },

  async descargarPDF(id: number) {
    const res = await api.get(`/facturas/${id}/pdf`, { responseType: 'blob' })
    return res.data as Blob
  },

  async delete(id: number) {
    const res = await api.delete<ApiResponse>(`/facturas/${id}`)
    return res.data
  },
}
