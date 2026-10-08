import api from './api'
import type { ApiResponse } from '@/types/auth'

export interface ExcelVersion {
  id: number
  tipo: string
  nombre: string
  version: number
  activo: boolean
  fecha: string | null
  usuario: string
}

export interface ExcelEstado {
  [tipo: string]: {
    activo: boolean
    nombre?: string
    version?: number
    tamano?: number
    fecha?: string
    total_versiones: number
  }
}

export const excelService = {
  async upload(tipo: 'clientes' | 'financiero' | 'cartera_creemos', file: File) {
    const form = new FormData()
    form.append('file', file)
    const res = await api.post<ApiResponse>(`/excel/upload?tipo=${tipo}`, form)
    return res.data
  },

  async getVersiones(tipo?: string) {
    const params: any = {}
    if (tipo) params.tipo = tipo
    const res = await api.get<ApiResponse<{items: ExcelVersion[]}>>('/excel/versiones', { params })
    return res.data
  },

  async restaurar(archivoId: number) {
    const res = await api.post<ApiResponse>(`/excel/restaurar/${archivoId}`)
    return res.data
  },

  async getEstado() {
    const res = await api.get<ApiResponse<ExcelEstado>>('/excel/estado')
    return res.data
  },

  async eliminarActivo(tipo: string) {
    const res = await api.delete<ApiResponse>(`/excel/activo/${tipo}`)
    return res.data
  },

  async actualizarExcelCartera() {
    const res = await api.post<ApiResponse<{
      bloque_nuevo: { label: string; filas: number; altas: number } | null
      pagos_excel: { escritos_bloque: number; escritos_hoja: number; omitidos: number }
      importacion: { clientes: number; prestamos: number; pagos: number }
    }>>('/sync/cartera/actualizar-excel')
    return res.data
  },

  async exportarTodo() {
    await descargar('/excel/exportar-todo', `respaldo_completo_${new Date().toISOString().slice(0, 10)}.xlsx`)
  },

  async descargarCartera() {
    await descargar('/excel/descargar-cartera', 'Creemos.xlsx')
  },
}

async function descargar(path: string, nombrePorDefecto: string) {
  const res = await api.get(path, { responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const a = document.createElement('a')
  a.href = url
  const match = res.headers['content-disposition']?.match(/filename="?(.+)"?/)
  a.download = match?.[1] || nombrePorDefecto
  a.click()
  window.URL.revokeObjectURL(url)
}
