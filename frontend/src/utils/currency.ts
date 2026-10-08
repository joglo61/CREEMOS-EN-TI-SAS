export function formatCOP(value: number | string): string {
  const num = typeof value === 'string' ? parseFloat(value.replace(/\./g, '').replace(/,/g, '')) : value
  if (isNaN(num)) return ''
  return Math.floor(num).toLocaleString('es-CO')
}

export function parseCOP(formatted: string): number {
  const cleaned = formatted.replace(/[^0-9]/g, '')
  return parseInt(cleaned, 10) || 0
}

export function formatCOPInput(value: string): string {
  const cleaned = value.replace(/[^0-9]/g, '')
  if (!cleaned) return ''
  return parseInt(cleaned, 10).toLocaleString('es-CO')
}
