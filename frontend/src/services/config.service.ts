import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface ConfigData {
  id: number
  empresa: string
  nit: string
  direccion: string | null
  telefono: string | null
  correo: string | null
  logo: string | null
  tasa_interes: number
  dias_gracia: number
  siguiente_factura: number
  ruta_recibos: string
  ruta_backups: string
}

export const configService = {
  async get() {
    const res = await api.get<ApiResponse<ConfigData>>('/config')
    return res.data
  },

  async update(data: Partial<ConfigData>) {
    const res = await api.put<ApiResponse<ConfigData>>('/config', data)
    return res.data
  },
}
