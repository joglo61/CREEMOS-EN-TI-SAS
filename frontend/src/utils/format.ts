export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '-'
  const parts = dateStr.split(/[T ]/)[0].split('-') // ISO ("…T…") o SQL ("… hh:mm")
  if (parts.length !== 3) return dateStr
  return `${parts[2]}/${parts[1]}/${parts[0]}`
}
