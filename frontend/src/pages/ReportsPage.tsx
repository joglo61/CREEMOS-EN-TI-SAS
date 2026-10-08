import { useState, useEffect } from 'react'
import api from '@/services/api'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area,
} from 'recharts'
import type { ValueType } from 'recharts/types/component/DefaultTooltipContent'
import { descargar } from '@/services/excel.service'

type Tab = 'cartera' | 'flujo' | 'clientes' | 'pagos' | 'ingresos' | 'mora' | 'facturas'

interface FilaCartera {
  prestamo_id: number
  fecha_desembolso: string
  placa: string
  cliente: string
  vr_credito: string
  vr_cuota: string
  saldo_anterior: string
  fecha_inicial: string
  fecha_final: string | null
  dias: number | null
  intereses: string
  interes_mora: string
  abono_capital: string
  cuota: string
  saldo_final: string
  pago_en_mes: boolean
  alta: boolean
  estado: string
}

interface CarteraData {
  mes: string
  items: FilaCartera[]
  totales: Record<string, string | number>
}

interface FlujoData {
  labels: string[]
  ingresos: number[]
  intereses: number[]
  capital_recuperado: number[]
  nuevos_prestamos: number[]
  flujo_neto: number[]
  saldo_final: number[]
}

const TABS: { key: Tab; label: string }[] = [
  { key: 'cartera', label: 'Cartera mensual' },
  { key: 'flujo', label: 'Flujo de Caja' },
  { key: 'clientes', label: 'Clientes' },
  { key: 'pagos', label: 'Pagos' },
  { key: 'ingresos', label: 'Ingresos' },
  { key: 'mora', label: 'Mora' },
  { key: 'facturas', label: 'Facturas' },
]

const fmt = (n: number | string) => `$${Number(n).toLocaleString('es-CO')}`
const fmtPct = (n: number) => n >= 0 ? `$${n.toLocaleString('es-CO')}` : `-$${Math.abs(n).toLocaleString('es-CO')}`
const tipFmt = (v: ValueType | undefined) => v != null ? fmt(Number(v)) : ''

function FlujoChart({ data }: { data: FlujoData }) {
  const chartData = data.labels.map((l, i) => ({
    mes: l,
    Ingresos: data.ingresos[i],
    Intereses: data.intereses[i],
    Capital: data.capital_recuperado[i],
    Prestamos: data.nuevos_prestamos[i],
    Neto: data.flujo_neto[i],
    Saldo: data.saldo_final[i],
  }))

  const totalIngresos = data.ingresos.reduce((a, b) => a + b, 0)
  const totalIntereses = data.intereses.reduce((a, b) => a + b, 0)
  const totalPrestamos = data.nuevos_prestamos.reduce((a, b) => a + b, 0)
  const netoTotal = totalIngresos - totalPrestamos

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <div className="card p-4">
          <p className="text-xs text-surface-500 uppercase">Ingresos Totales</p>
          <p className="text-2xl font-bold text-green-600">{fmt(totalIngresos)}</p>
        </div>
        <div className="card p-4">
          <p className="text-xs text-surface-500 uppercase">Intereses Cobrados</p>
          <p className="text-2xl font-bold text-primary-600">{fmt(totalIntereses)}</p>
        </div>
        <div className="card p-4">
          <p className="text-xs text-surface-500 uppercase">Nuevos Préstamos</p>
          <p className="text-2xl font-bold text-red-600">{fmt(totalPrestamos)}</p>
        </div>
        <div className="card p-4">
          <p className="text-xs text-surface-500 uppercase">Flujo Neto</p>
          <p className={`text-2xl font-bold ${netoTotal >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {fmtPct(netoTotal)}
          </p>
        </div>
      </div>

      {/* Chart 1: Ingresos vs Nuevos Préstamos (Bar) */}
      <div className="card p-4">
        <h3 className="mb-4 text-sm font-semibold text-surface-600 uppercase">Ingresos vs Nuevos Préstamos</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={(v) => `$${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={tipFmt} />
            <Legend />
            <Bar dataKey="Ingresos" fill="#16a34a" name="Ingresos" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Prestamos" fill="#dc2626" name="Nuevos Préstamos" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Chart 2: Intereses vs Capital (Stacked Bar) */}
      <div className="card p-4">
        <h3 className="mb-4 text-sm font-semibold text-surface-600 uppercase">Composición de Ingresos</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={(v) => `$${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={tipFmt} />
            <Legend />
            <Bar dataKey="Intereses" stackId="a" fill="#2563eb" name="Intereses" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Capital" stackId="a" fill="#16a34a" name="Capital Recuperado" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Chart 3: Flujo Neto (Bar + Line) */}
      <div className="card p-4">
        <h3 className="mb-4 text-sm font-semibold text-surface-600 uppercase">Flujo Neto del Mes</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={(v) => `$${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={tipFmt} />
            <Legend />
            <Bar dataKey="Neto" fill="#8b5cf6" name="Flujo Neto" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Chart 4: Saldo Total (Area) */}
      <div className="card p-4">
        <h3 className="mb-4 text-sm font-semibold text-surface-600 uppercase">Saldo Total en Cartera</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" tick={{ fontSize: 11 }} />
            <YAxis tickFormatter={(v) => `$${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={tipFmt} />
            <Legend />
            <Area type="monotone" dataKey="Saldo" stroke="#2563eb" fill="#dbeafe" name="Saldo en Cartera" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

const fdate = (s: string | null) => (s ? s.split('-').reverse().join('/') : '-')

// Reemplazo del bloque mensual CXCOBRAR del Excel
function CarteraMensual() {
  const hoy = new Date()
  const [mes, setMes] = useState(`${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, '0')}`)
  const [data, setData] = useState<CarteraData | null>(null)
  const [soloPendientes, setSoloPendientes] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [anio, numMes] = mes.split('-').map(Number)

  useEffect(() => {
    if (!anio || !numMes) return
    setLoading(true)
    setError('')
    api.get('/reportes/cartera-mensual', { params: { anio, mes: numMes } })
      .then((res) => setData(res.data.data))
      .catch((err) => setError(err?.response?.data?.detail || 'Error al cargar la cartera.'))
      .finally(() => setLoading(false))
  }, [anio, numMes])

  const t = data?.totales
  const filas = (data?.items || []).filter((f) => !soloPendientes || !f.pago_en_mes)

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <label htmlFor="cartera-mes" className="block text-xs font-medium text-surface-500">Mes</label>
          <input id="cartera-mes" type="month" value={mes} onChange={(e) => setMes(e.target.value)} className="input w-44" />
        </div>
        <label className="flex items-center gap-2 pb-2 text-sm text-surface-600">
          <input type="checkbox" checked={soloPendientes} onChange={(e) => setSoloPendientes(e.target.checked)} />
          Solo los que no han pagado
        </label>
        <button
          onClick={() => descargar('/reportes/cartera-mensual/excel', `cartera_${mes}.xlsx`, { anio, mes: numMes })
            .catch(() => alert('Error al exportar.'))}
          className="btn-success ml-auto"
        >
          Exportar a Excel
        </button>
      </div>

      {error && <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      {t && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {[
            ['Recaudo del mes', fmt(t.recaudo)],
            ['Abono a capital', fmt(t.abono_capital)],
            ['Abono intereses', fmt(t.abono_intereses)],
            ['Saldo al cierre', fmt(t.saldo_final)],
            ['Pagaron', `${t.pagaron} de ${t.creditos}`],
          ].map(([label, valor]) => (
            <div key={label} className="card p-4">
              <p className="text-xs font-medium uppercase tracking-wider text-surface-500">{label}</p>
              <p className="mt-1 text-xl font-bold text-surface-900">{valor}</p>
            </div>
          ))}
        </div>
      )}

      <div className="table-wrap">
        {loading ? (
          <div className="p-12 text-center text-sm text-surface-400">Cargando...</div>
        ) : !filas.length ? (
          <div className="p-8 text-center text-sm text-surface-400">Sin créditos en este mes.</div>
        ) : (
          <table>
            <caption className="sr-only">Cartera por cobrar de {data?.mes}; las filas sombreadas pagaron en el mes</caption>
            <thead>
              <tr>
                {['Desembolso', 'Placa', 'Cliente', 'Saldo anterior', 'Fecha pago', 'Días', 'Intereses', 'Mora', 'Abono K', 'Cuota', 'Saldo final', ''].map((h) => (
                  <th key={h} className="whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filas.map((f) => (
                <tr key={f.prestamo_id} className={f.pago_en_mes ? 'bg-primary-50/60' : ''}>
                  <td className="whitespace-nowrap">{fdate(f.fecha_desembolso)}</td>
                  <td className="whitespace-nowrap font-mono">{f.placa}</td>
                  <td className="whitespace-nowrap">{f.cliente}</td>
                  <td className="text-right">{fmt(f.saldo_anterior)}</td>
                  <td className="whitespace-nowrap">{fdate(f.fecha_final)}</td>
                  <td className="text-right">{f.dias ?? '-'}</td>
                  <td className="text-right">{f.pago_en_mes ? fmt(f.intereses) : '-'}</td>
                  <td className="text-right">{Number(f.interes_mora) ? fmt(f.interes_mora) : '-'}</td>
                  <td className="text-right">{f.pago_en_mes ? fmt(f.abono_capital) : '-'}</td>
                  <td className="text-right font-medium">{f.pago_en_mes ? fmt(f.cuota) : '-'}</td>
                  <td className="text-right font-semibold">{fmt(f.saldo_final)}</td>
                  <td>
                    {f.pago_en_mes ? <span className="badge-green">Pagó</span>
                      : f.alta ? <span className="badge-blue">Nuevo</span>
                      : <span className="badge-yellow">Pendiente</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function TableReport({ reporte }: { reporte: string }) {
  const [desde, setDesde] = useState('')
  const [hasta, setHasta] = useState('')
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const hasDateFilter = ['pagos', 'ingresos', 'facturas'].includes(reporte)

  const load = async () => {
    setLoading(true)
    setError('')
    try {
      const params: any = {}
      if (desde) params.desde = desde
      if (hasta) params.hasta = hasta
      const res = await api.get(`/reportes/${reporte}`, { params })
      if (res.data.success) {
        setItems(res.data.data.items || [])
        setTotal(res.data.data.total ?? null)
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Error al cargar reporte.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { if (!hasDateFilter) load() }, [reporte])

  const renderHeaders = () => {
    if (!items.length) return null
    return Object.keys(items[0]).map((k) => (
      <th key={k} className="whitespace-nowrap border-b px-3 py-2 text-left text-xs font-medium uppercase text-surface-500">
        {k.replace(/_/g, ' ')}
      </th>
    ))
  }

  const renderCell = (val: any) => {
    if (val === null || val === undefined) return '-'
    if (typeof val === 'string' && /^\d+$/.test(val)) return fmt(Number(val))
    if (typeof val === 'number') return fmt(val)
    return String(val)
  }

  return (
    <div>
      {hasDateFilter && (
        <div className="mb-4 flex flex-wrap items-end gap-3">
          <div>
            <label className="block text-xs text-surface-500">Desde</label>
            <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)}
              className="rounded border px-2 py-1 text-sm" />
          </div>
          <div>
            <label className="block text-xs text-surface-500">Hasta</label>
            <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)}
              className="rounded border px-2 py-1 text-sm" />
          </div>
          <button onClick={load} disabled={loading}
            className="btn-primary">
            {loading ? 'Consultando...' : 'Consultar'}
          </button>
        </div>
      )}

      {error && <div className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      {total !== null && (
        <p className="mb-3 text-sm font-semibold">Total: {fmt(total)}</p>
      )}

      <div className="card overflow-x-auto">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-sm text-surface-400">Cargando...</div>
        ) : items.length === 0 ? (
          <div className="p-8 text-center text-sm text-surface-400">Sin datos disponibles.</div>
        ) : (
          <table className="min-w-full text-sm">
            <thead className="bg-surface-50">{renderHeaders()}</thead>
            <tbody>
              {items.map((row, i) => (
                <tr key={i} className="border-b hover:bg-surface-50">
                  {Object.keys(items[0]).map((k) => (
                    <td key={k} className="whitespace-nowrap px-3 py-2">{renderCell(row[k])}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <button onClick={() => descargar('/reportes/exportar-excel', `reporte_${reporte}.xlsx`, { reporte }).catch(() => alert('Error al exportar.'))}
        className="mt-4 btn-success">
        Exportar a Excel
      </button>
    </div>
  )
}

export default function ReportsPage() {
  const [tab, setTab] = useState<Tab>('cartera')
  const [flujo, setFlujo] = useState<FlujoData | null>(null)
  const [flujoLoading, setFlujoLoading] = useState(true)

  useEffect(() => {
    if (tab === 'flujo') {
      setFlujoLoading(true)
      api.get('/reportes/flujo-mensual?meses=12').then((res) => {
        if (res.data.success) setFlujo(res.data.data)
      }).catch(() => {}).finally(() => setFlujoLoading(false))
    }
  }, [tab])

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="mb-6 text-2xl font-bold text-surface-800">Reportes</h1>

      {/* Tabs */}
      <div className="mb-6 flex flex-wrap gap-2">
        {TABS.map((t) => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
              tab === t.key ? 'bg-primary-600 text-white' : 'bg-white text-surface-600 hover:bg-surface-100 shadow'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'cartera' ? (
        <CarteraMensual />
      ) : tab === 'flujo' ? (
        flujoLoading ? (
          <div className="flex items-center justify-center p-20 text-sm text-surface-400">Cargando gráficos...</div>
        ) : flujo ? (
          <FlujoChart data={flujo} />
        ) : (
          <div className="text-center text-sm text-surface-400">Error al cargar datos de flujo de caja.</div>
        )
      ) : (
        <TableReport reporte={tab} />
      )}
    </div>
  )
}
