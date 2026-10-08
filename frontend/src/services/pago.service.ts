import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface PagoItem {
  id: number
  prestamo_id: number
  numero_factura: string
  fecha_pago: string
  dias_calculados: number
  dias_mora: number
  saldo_anterior: string
  intereses: string
  intereses_mora: string
  capital: string
  valor_pagado: string
  saldo_nuevo: string
  observaciones: string | null
  usuario_nombre: string
  tasa_interes_aplicada: string | null
  created_at: string | null
}

export interface PagoRegistrarResponse {
  pago: PagoItem
  factura: string
  factura_id: number
}

export interface PagoPreview {
  prestamo_id: number
  valor_pagado: string
  fecha_pago: string
  dias_calculados: number
  dias_mora: number
  saldo_anterior: string
  intereses: string
  intereses_mora: string
  intereses_totales: string
  capital: string
  saldo_nuevo: string
  aplicar_interes?: boolean
  tasa_interes_aplicada?: string | null
}

export const pagoService = {
  async calcular(data: { prestamo_id: number; valor_pagado: number; fecha_pago: string; aplicar_interes?: boolean; tasa_interes?: number | null }) {
    const res = await api.post<ApiResponse<PagoPreview>>('/pagos/calcular', data)
    return res.data
  },

  async registrar(data: { prestamo_id: number; valor_pagado: number; fecha_pago: string; observaciones?: string; aplicar_interes?: boolean; tasa_interes?: number | null }) {
    const res = await api.post<ApiResponse<PagoRegistrarResponse>>('/pagos/registrar', data)
    return res.data
  },

  async list(params: { prestamo_id?: number; page?: number; page_size?: number }) {
    const res = await api.get<ApiResponse<{items: PagoItem[]}>>('/pagos', { params })
    return res.data
  },

  async getById(id: number) {
    const res = await api.get<ApiResponse<PagoItem>>(`/pagos/${id}`)
    return res.data
  },
}
