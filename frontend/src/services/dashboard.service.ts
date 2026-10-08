import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface DashboardData {
  clientes_activos: number
  prestamos_mora: number
  capital_pendiente: number
  ingresos_hoy: number
  ingresos_semana: number
  ingresos_mes: number
  ultimos_pagos: { id: number; factura: string; cliente: string; valor: string; fecha: string }[]
  ultimas_facturas: { id: number; numero: string; cliente: string; fecha: string; estado: string }[]
}

export const dashboardService = {
  async get() {
    const res = await api.get<ApiResponse<DashboardData>>('/dashboard')
    return res.data
  },
}
