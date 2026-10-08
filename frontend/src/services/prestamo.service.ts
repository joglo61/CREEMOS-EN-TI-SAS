import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface PrestamoItem {
  id: number
  cliente_id: number
  cliente_nombre: string
  cliente_placa: string
  capital_inicial: string
  saldo_actual: string
  valor_cuota: string
  tasa_interes: string
  fecha_inicio: string
  fecha_primer_pago: string
  fecha_proximo_pago: string
  estado: string
  created_at: string | null
  updated_at: string | null
}

export interface PrestamoCreateData {
  cliente_id: number
  capital_inicial: number
  valor_cuota: number
  fecha_inicio: string
  fecha_primer_pago?: string
}

export const prestamoService = {
  async list(params: { search?: string; estado?: string; page?: number; page_size?: number }) {
    const res = await api.get<ApiResponse<{items: PrestamoItem[]; total: number}>>('/prestamos', { params })
    return res.data
  },

  async getById(id: number) {
    const res = await api.get<ApiResponse<PrestamoItem>>(`/prestamos/${id}`)
    return res.data
  },

  async create(data: PrestamoCreateData) {
    const res = await api.post<ApiResponse<{prestamo: PrestamoItem}>>('/prestamos', data)
    return res.data
  },

  async update(id: number, data: { valor_cuota?: number; estado?: string }) {
    const res = await api.put<ApiResponse<PrestamoItem>>(`/prestamos/${id}`, data)
    return res.data
  },

  async getCronograma(id: number) {
    const res = await api.get<ApiResponse<{items: CronogramaEntry[]}>>(`/prestamos/${id}/cronograma`)
    return res.data
  },

  async actualizarEstado(id: number) {
    const res = await api.post<ApiResponse<{estado: string}>>(`/prestamos/${id}/actualizar-estado`)
    return res.data
  },

  async toggleCronogramaEstado(prestamoId: number, cronogramaId: number) {
    const res = await api.post<ApiResponse<{estado: string}>>(`/prestamos/${prestamoId}/cronograma/${cronogramaId}/toggle-estado`)
    return res.data
  },

  async anular(id: number) {
    const res = await api.post<ApiResponse<{estado: string}>>(`/prestamos/${id}/anular`)
    return res.data
  },
}

export interface CronogramaEntry {
  id: number
  prestamo_id: number
  numero_cuota: number
  fecha_estimada: string
  capital_estimado: string
  interes_estimado: string
  valor_estimado: string
  saldo_estimado: string
  estado: string
}
