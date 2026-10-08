import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface SyncImportados {
  clientes: number
  prestamos: number
  pagos: number
  eliminados: number
  errores: string[]
}

export interface SyncResult {
  creados?: number
  actualizados?: number
  errores?: number
  status?: string
  clientes?: number
  creditos?: number
  pagos?: number
  snapshots?: number
  discrepancias?: number
  importados?: SyncImportados
}

export interface SyncHistorialItem {
  id: number
  accion: string
  descripcion: string | null
  usuario: string
  fecha: string | null
}

export const syncService = {
  async sincronizar(tipo: 'clientes' | 'financiero' | 'cartera') {
    const res = await api.post<ApiResponse<SyncResult>>(`/sync/sincronizar?tipo=${tipo}`)
    return res.data
  },

  async exportarPagos(dias: number = 30) {
    const res = await api.post<ApiResponse>(`/sync/exportar-pagos?dias=${dias}`)
    return res.data
  },

  async getHistorial() {
    const res = await api.get<ApiResponse<{items: SyncHistorialItem[]}>>('/sync/historial')
    return res.data
  },

  async guardarEnExcel() {
    const res = await api.post<ApiResponse>('/excel/guardar')
    return res.data
  },
}
