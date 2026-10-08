import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface UsuarioItem {
  id: number
  nombre: string
  usuario: string
  rol: string
  activo: boolean
  intentos_fallidos: number
  bloqueado_hasta: string | null
  ultimo_acceso: string | null
  created_at: string | null
}

export const usuarioService = {
  async list() {
    const res = await api.get<ApiResponse<{items: UsuarioItem[]}>>('/usuarios')
    return res.data
  },

  async create(data: { nombre: string; usuario: string; password: string; rol: string }) {
    const res = await api.post<ApiResponse>('/usuarios', data)
    return res.data
  },

  async update(id: number, data: { nombre?: string; rol?: string; activo?: boolean }) {
    const res = await api.put<ApiResponse>(`/usuarios/${id}`, data)
    return res.data
  },

  async cambiarPassword(id: number, password: string) {
    const res = await api.post<ApiResponse>(`/usuarios/${id}/cambiar-password`, { password })
    return res.data
  },

  async desbloquear(id: number) {
    const res = await api.post<ApiResponse<UsuarioItem>>(`/usuarios/${id}/desbloquear`)
    return res.data
  },
}
