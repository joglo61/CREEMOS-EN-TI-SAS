import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { dashboardService, type DashboardData } from '@/services/dashboard.service'
import api from '@/services/api'
import { formatDate } from '@/utils/format'
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts'
import type { ValueType } from 'recharts/types/component/DefaultTooltipContent'

const tipFmt = (v: ValueType | undefined) => v != null ? `$${Number(v).toLocaleString('es-CO')}` : ''

const cardIcons = [
  'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
  'M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z',
  'M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 003 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z',
  'M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  'M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z',
  'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z',
]

export default function DashboardPage() {
  const navigate = useNavigate()
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [errorMsg, setErrorMsg] = useState('')
  const [chartData, setChartData] = useState<{ mes: string; Ingresos: number }[]>([])

  useEffect(() => {
    dashboardService.get().then((res) => {
      if (res.success && res.data) setData(res.data)
      else setErrorMsg('No se pudieron cargar los indicadores.')
      setLoading(false)
    }).catch((err) => {
      setErrorMsg(err?.response?.data?.detail || err?.message || 'Error de conexión con el servidor.')
      setLoading(false)
    })

    api.get('/reportes/flujo-mensual?meses=6').then((res) => {
      if (res.data.success) {
        const d = res.data.data
        setChartData(d.labels.map((l: string, i: number) => ({ mes: l, Ingresos: d.ingresos[i] })))
      }
    }).catch(() => {})
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-primary-200 border-t-primary-600" />
          <p className="text-sm font-medium text-surface-400">Cargando indicadores...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="rounded-xl bg-red-50 border border-red-200 px-6 py-4 text-sm text-red-700">
          {errorMsg || 'Error al cargar dashboard.'}
        </div>
      </div>
    )
  }

  const cop = (n: number) => `$${n.toLocaleString('es-CO')}`
  // Color con significado: rojo = mora (solo si hay), verde = ingresos, azul = cartera
  const tonos = {
    azul: 'bg-primary-50 text-primary-600',
    rojo: 'bg-red-50 text-red-600',
    verde: 'bg-emerald-50 text-emerald-600',
    neutro: 'bg-surface-100 text-surface-500',
  }
  const cards = [
    { label: 'Clientes Activos', value: data.clientes_activos, link: '/clientes', tono: tonos.azul },
    { label: 'Préstamos en Mora', value: data.prestamos_mora, link: '/prestamos?estado=MORA', tono: data.prestamos_mora > 0 ? tonos.rojo : tonos.neutro, alerta: data.prestamos_mora > 0 },
    { label: 'Capital Pendiente', value: cop(data.capital_pendiente), link: '/prestamos', tono: tonos.azul },
    { label: 'Ingresos Hoy', value: cop(data.ingresos_hoy), link: '/facturas', tono: tonos.verde },
    { label: 'Ingresos Semana', value: cop(data.ingresos_semana), link: '/facturas', tono: tonos.verde },
    { label: 'Ingresos del Mes', value: cop(data.ingresos_mes), link: '/facturas', tono: tonos.verde },
  ]

  return (
    <div className="p-6 lg:p-8 animate-fade-in">
      <div className="mb-8">
        <h1 className="page-title">Dashboard</h1>
        <p className="mt-1 text-sm text-surface-400">Resumen general del sistema</p>
      </div>

      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {cards.map((c, i) => (
          <button
            key={c.label}
            onClick={() => navigate(c.link)}
            className={`card-hover p-4 text-left focus:outline-none focus:ring-2 focus:ring-primary-500 ${c.alerta ? 'border-red-200' : ''}`}
          >
            <span className={`mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg ${c.tono}`}>
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.75} aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" d={cardIcons[i]} />
              </svg>
            </span>
            <p className="text-xs font-medium uppercase tracking-wider text-surface-500">{c.label}</p>
            <p className={`mt-1 text-2xl font-bold tracking-tight ${c.alerta ? 'text-red-600' : 'text-surface-900'}`}>{c.value}</p>
          </button>
        ))}
      </div>

      {chartData.length > 0 && (
        <div className="mb-8 card p-6">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-surface-500 uppercase tracking-wider">Ingresos Mensuales</h3>
              <p className="text-xs text-surface-400">Últimos 6 meses</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData}>
              <XAxis dataKey="mes" tick={{ fontSize: 12, fill: '#64748b' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                formatter={tipFmt}
                contentStyle={{
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                  fontSize: '13px',
                }}
              />
              <Bar dataKey="Ingresos" fill="#2563eb" radius={[6, 6, 0, 0]} maxBarSize={40} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card p-5">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-surface-500 uppercase tracking-wider">Últimos Ingresos</h3>
            <span className="badge-blue text-[10px]">{data.ultimos_pagos.length}</span>
          </div>
          {data.ultimos_pagos.length === 0 ? (
            <p className="py-8 text-center text-sm text-surface-400">Sin pagos recientes.</p>
          ) : (
            <div className="space-y-1">
              {data.ultimos_pagos.map((p) => (
                <div key={p.id} className="flex items-center justify-between rounded-lg px-3 py-2.5 transition-colors hover:bg-surface-50">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-surface-800 truncate">{p.cliente}</p>
                    <p className="text-xs text-surface-400">{p.factura} &middot; {formatDate(p.fecha)}</p>
                  </div>
                  <span className="ml-3 text-sm font-bold text-emerald-600">${Number(p.valor).toLocaleString('es-CO')}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card p-5">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-surface-500 uppercase tracking-wider">Últimas Facturas</h3>
            <span className="badge-blue text-[10px]">{data.ultimas_facturas.length}</span>
          </div>
          {data.ultimas_facturas.length === 0 ? (
            <p className="py-8 text-center text-sm text-surface-400">Sin facturas recientes.</p>
          ) : (
            <div className="space-y-1">
              {data.ultimas_facturas.map((f) => (
                <div key={f.id} className="flex items-center justify-between rounded-lg px-3 py-2.5 transition-colors hover:bg-surface-50">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-surface-800 truncate">{f.cliente}</p>
                    <p className="text-xs text-surface-400">{f.numero} &middot; {formatDate(f.fecha)}</p>
                  </div>
                  <span className={`badge ml-3 text-[10px] ${f.estado === 'EMITIDA' ? 'badge-blue' : 'badge-gray'}`}>{f.estado}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
