import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface ClienteListado {
  id: number
  nombre: string
  cedula: string
  placa: string
  telefono: string | null
  direccion: string | null
  correo: string | null
  estado: string
  observaciones: string | null
  created_at: string | null
  updated_at: string | null
}

export interface ClienteDetalle extends ClienteListado {
  prestamo: {
    id: number
    capital_inicial: string
    saldo_actual: string
    valor_cuota: string
    tasa_interes: string
    fecha_inicio: string
    fecha_proximo_pago: string
    estado: string
  } | null
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

export interface HistorialEntry {
  id: number
  accion: string
  modulo: string | null
  descripcion: string | null
  usuario: string | null
  created_at: string | null
}

export interface ClienteCreateData {
  nombre: string
  cedula: string
  placa: string
  telefono?: string
  direccion?: string
  correo?: string
  observaciones?: string
  capital_inicial: number
  valor_cuota: number
  fecha_inicio: string
  fecha_primer_pago?: string
}

export interface ClienteUpdateData {
  nombre?: string
  telefono?: string
  direccion?: string
  correo?: string
  observaciones?: string
}

export const clienteService = {
  async list(params: { search?: string; estado?: string; page?: number; page_size?: number }) {
    const res = await api.get<ApiResponse<{items: ClienteListado[]; total: number}>>('/clientes', { params })
    return res.data
  },

  async getById(id: number) {
    const res = await api.get<ApiResponse<ClienteDetalle>>(`/clientes/${id}`)
    return res.data
  },

  async create(data: ClienteCreateData) {
    const res = await api.post<ApiResponse<ClienteDetalle>>('/clientes', data)
    return res.data
  },

  async update(id: number, data: ClienteUpdateData) {
    const res = await api.put<ApiResponse<ClienteDetalle>>(`/clientes/${id}`, data)
    return res.data
  },

  async delete(id: number) {
    const res = await api.delete<ApiResponse>(`/clientes/${id}`)
    return res.data
  },

  async hardDelete(id: number) {
    const res = await api.delete<ApiResponse>(`/clientes/${id}/hard`)
    return res.data
  },

  async toggleEstado(id: number) {
    const res = await api.post<ApiResponse<{estado: string}>>(`/clientes/${id}/toggle-estado`)
    return res.data
  },

  async getCronograma(id: number) {
    const res = await api.get<ApiResponse<{items: CronogramaEntry[]}>>(`/clientes/${id}/cronograma`)
    return res.data
  },

  async getHistorial(id: number) {
    const res = await api.get<ApiResponse<{items: HistorialEntry[]}>>(`/clientes/${id}/historial`)
    return res.data
  },
}
