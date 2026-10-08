import api from './api'

export const excelService = {
  async exportarTodo() {
    await descargar('/excel/exportar-todo', `respaldo_completo_${new Date().toISOString().slice(0, 10)}.xlsx`)
  },
}

export async function descargar(path: string, nombrePorDefecto: string, params?: Record<string, unknown>) {
  const res = await api.get(path, { responseType: 'blob', params })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const a = document.createElement('a')
  a.href = url
  const match = res.headers['content-disposition']?.match(/filename="?([^"]+)"?/)
  a.download = match?.[1] || nombrePorDefecto
  a.click()
  window.URL.revokeObjectURL(url)
}
