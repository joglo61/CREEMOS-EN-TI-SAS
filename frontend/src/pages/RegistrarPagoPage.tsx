import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { pagoService, type PagoPreview } from '@/services/pago.service'
import { prestamoService } from '@/services/prestamo.service'
import { useUnsaved } from '@/contexts/UnsavedContext'
import CurrencyInput from '@/components/CurrencyInput'

export default function RegistrarPagoPage() {
  const { setDirty } = useUnsaved()
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [loadingLoan, setLoadingLoan] = useState(true)
  const [error, setError] = useState('')
  const [result, setResult] = useState<any>(null)
  const [preview, setPreview] = useState<PagoPreview | null>(null)
  const [confirmPreview, setConfirmPreview] = useState<PagoPreview | null>(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState({
    valor_pagado: 0,
    fecha_pago: '',
    observaciones: '',
  })
  const [aplicarInteres, setAplicarInteres] = useState(true)
  const [tasaInteres, setTasaInteres] = useState(2.5)
  const [calculandoPreview, setCalculandoPreview] = useState(false)

  const recalcular = useCallback(async (valor: number, fecha: string, aplicar: boolean, tasa: number) => {
    if (valor <= 0 || !fecha) { setPreview(null); return }
    setCalculandoPreview(true)
    try {
      const res = await pagoService.calcular({
        prestamo_id: Number(id), valor_pagado: valor, fecha_pago: fecha,
        aplicar_interes: aplicar, tasa_interes: aplicar ? tasa : null,
      })
      if (res.success && res.data) setPreview(res.data)
    } catch {
      setPreview(null)
    } finally {
      setCalculandoPreview(false)
    }
  }, [id])

  useEffect(() => {
    if (!id) return
    prestamoService.getById(Number(id)).then((res) => {
      if (res.success && res.data) {
        const loan = res.data as any
        const cuota = Number(loan.valor_cuota)
        setForm((prev) => ({
          ...prev,
          valor_pagado: cuota || 0,
          fecha_pago: loan.fecha_proximo_pago,
        }))
        if (cuota > 0 && loan.fecha_proximo_pago) {
          recalcular(cuota, loan.fecha_proximo_pago, true, 2.5)
        }
      }
      setLoadingLoan(false)
    }).catch(() => setLoadingLoan(false))
  }, [id])

  const handleValorChange = (valor: number) => {
    setForm((prev) => ({ ...prev, valor_pagado: valor }))
    if (valor > 0 && form.fecha_pago) {
      recalcular(valor, form.fecha_pago, aplicarInteres, tasaInteres)
    } else {
      setPreview(null)
    }
  }

  const handleFechaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const fecha = e.target.value
    setForm((prev) => ({ ...prev, fecha_pago: fecha }))
    if (form.valor_pagado > 0 && fecha) {
      recalcular(form.valor_pagado, fecha, aplicarInteres, tasaInteres)
    } else {
      setPreview(null)
    }
  }

  const handleToggleInteres = () => {
    const nuevo = !aplicarInteres
    setAplicarInteres(nuevo)
    if (form.valor_pagado > 0 && form.fecha_pago) {
      recalcular(form.valor_pagado, form.fecha_pago, nuevo, nuevo ? tasaInteres : 0)
    }
  }

  const handleTasaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value)
    const tasa = isNaN(val) ? 0 : val
    setTasaInteres(tasa)
    if (form.valor_pagado > 0 && form.fecha_pago && aplicarInteres) {
      recalcular(form.valor_pagado, form.fecha_pago, true, tasa)
    }
  }

  const openConfirmModal = async () => {
    setError('')
    if (!form.valor_pagado || form.valor_pagado <= 0) { setError('Ingrese un valor válido.'); return }
    if (!form.fecha_pago) { setError('Seleccione una fecha.'); return }
    const p = preview
    if (p) { setConfirmPreview(p); setModalOpen(true); return }
    setCalculandoPreview(true)
    try {
      const res = await pagoService.calcular({
        prestamo_id: Number(id), valor_pagado: form.valor_pagado, fecha_pago: form.fecha_pago,
        aplicar_interes: aplicarInteres, tasa_interes: aplicarInteres ? tasaInteres : null,
      })
      if (res.success && res.data) {
        setConfirmPreview(res.data)
        setModalOpen(true)
      } else {
        setError('No se pudo calcular el pago. Verifica los valores.')
      }
    } catch {
      setError('Error al calcular el pago.')
    } finally {
      setCalculandoPreview(false)
    }
  }

  const handleConfirmarPago = async () => {
    setLoading(true)
    try {
      const res = await pagoService.registrar({
        prestamo_id: Number(id), valor_pagado: form.valor_pagado,
        fecha_pago: form.fecha_pago, observaciones: form.observaciones || undefined,
        aplicar_interes: aplicarInteres, tasa_interes: aplicarInteres ? tasaInteres : null,
      })
      if (res.success && res.data) { setResult(res.data); setDirty(); setModalOpen(false) }
      else { setError('Error al registrar el pago.'); setModalOpen(false) }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Error al registrar el pago.')
      setModalOpen(false)
    } finally {
      setLoading(false)
    }
  }

  if (loadingLoan) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-primary-200 border-t-primary-600" />
      </div>
    )
  }

  if (result) {
    return (
      <div className="p-6 lg:p-8 max-w-lg mx-auto animate-scale-in">
        <div className="card p-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100">
            <svg className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-surface-900">Pago Registrado</h2>
          <p className="mt-2 text-sm text-surface-400">Factura: <span className="font-mono font-bold text-primary-600">{result.factura}</span></p>
          <div className="mt-6 space-y-2 text-sm text-left border-t border-surface-100 pt-4">
            <Row label="Valor Pagado" value={`$${Number(result.pago.valor_pagado).toLocaleString('es-CO')}`} bold />
            <Row label="Intereses" value={`$${Number(result.pago.intereses).toLocaleString('es-CO')}`} />
            {result.pago.tasa_interes_aplicada !== null && result.pago.tasa_interes_aplicada !== undefined && (
              <Row label="Tasa aplicada" value={`${Number(result.pago.tasa_interes_aplicada)}%`} />
            )}
            {Number(result.pago.intereses_mora) > 0 && <Row label="Intereses de Mora" value={`$${Number(result.pago.intereses_mora).toLocaleString('es-CO')}`} danger />}
            <Row label="Abono a Capital" value={`$${Number(result.pago.capital).toLocaleString('es-CO')}`} />
            <Row label="Saldo Anterior" value={`$${Number(result.pago.saldo_anterior).toLocaleString('es-CO')}`} />
            <Row label="Saldo Nuevo" value={`$${Number(result.pago.saldo_nuevo).toLocaleString('es-CO')}`} bold />
          </div>
          <div className="mt-6 flex justify-center gap-3">
            <button onClick={() => navigate(`/prestamos/${id}`)} className="btn-primary">Ver Préstamo</button>
            <button onClick={() => navigate(`/facturas/${result.factura_id}`)} className="btn-secondary">Ver Recibo</button>
            <button onClick={() => { setResult(null); setPreview(null); setForm({ valor_pagado: 0, fecha_pago: '', observaciones: '' }) }} className="btn-ghost">Nuevo Pago</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 lg:p-8 max-w-lg mx-auto animate-fade-in">
      <button onClick={() => navigate(`/prestamos/${id}`)} className="mb-4 text-sm text-primary-600 hover:text-primary-700 font-medium">&larr; Volver al Préstamo</button>
      <h1 className="page-title mb-1">Registrar Pago</h1>
      <p className="text-sm text-surface-400 mb-6">Préstamo #{id}</p>

      {error && <div className="mb-4 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">{error}</div>}

      <div className="card p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1">Valor a Pagar *</label>
          <CurrencyInput
            value={form.valor_pagado}
            onChange={handleValorChange}
            className="input text-lg font-medium"
            placeholder="0"
          />
        </div>

        <div className="flex items-center justify-between rounded-xl bg-surface-50 p-3 border border-surface-200">
          <div>
            <p className="text-sm font-medium text-surface-700">Activar Interés</p>
            <p className="text-xs text-surface-400">{aplicarInteres ? `Tasa: ${tasaInteres}%` : 'Solo capital, sin interés'}</p>
          </div>
          <button
            type="button"
            role="switch"
            aria-checked={aplicarInteres}
            onClick={handleToggleInteres}
            className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors ${
              aplicarInteres ? 'bg-primary-600' : 'bg-surface-300'
            }`}
          >
            <span
              className={`inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform ${
                aplicarInteres ? 'translate-x-5' : 'translate-x-0'
              }`}
            />
          </button>
        </div>

        {aplicarInteres && (
          <div>
            <label className="block text-sm font-medium text-surface-700 mb-1">Tasa de Interés (%)</label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={tasaInteres}
                onChange={handleTasaChange}
                className="input w-24 text-center font-mono text-base"
              />
              <span className="text-sm text-surface-500">% mensual</span>
            </div>
            <p className="mt-1 text-xs text-surface-400">0% = todo el valor va a capital</p>
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1">Fecha de Pago *</label>
          <input type="date" value={form.fecha_pago} onChange={handleFechaChange} className="input" />
          <p className="mt-1 text-xs text-surface-400">Pre-cargada con la fecha del próximo pago. Puedes cambiarla.</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1">Observaciones</label>
          <textarea value={form.observaciones} onChange={(e) => setForm((prev) => ({ ...prev, observaciones: e.target.value }))} rows={2} className="input" />
        </div>

        {calculandoPreview && (
          <div className="flex items-center justify-center gap-2 text-sm text-surface-400">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-200 border-t-primary-600" />
            Calculando...
          </div>
        )}

        {preview && !calculandoPreview && (
          <div className="rounded-xl bg-surface-50 p-4 text-sm space-y-1.5 border border-surface-200">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-surface-500">Resumen del Cálculo</p>
            <div className="flex justify-between"><span className="text-surface-500">Días:</span><span>{preview.dias_calculados} ({preview.dias_mora > 0 ? `${preview.dias_mora} en mora` : 'sin mora'})</span></div>
            <div className="flex justify-between"><span className="text-surface-500">Intereses:</span><span>${Number(preview.intereses).toLocaleString('es-CO')}</span></div>
            {preview.tasa_interes_aplicada !== undefined && preview.tasa_interes_aplicada !== null && (
              <div className="flex justify-between text-surface-400 text-xs"><span>Tasa aplicada:</span><span>{Number(preview.tasa_interes_aplicada)}%</span></div>
            )}
            {Number(preview.intereses_mora) > 0 && (
              <div className="flex justify-between text-red-600"><span>Intereses Mora:</span><span>${Number(preview.intereses_mora).toLocaleString('es-CO')}</span></div>
            )}
            <div className="flex justify-between font-medium border-t border-surface-200 pt-1"><span>Intereses Totales:</span><span>${Number(preview.intereses_totales).toLocaleString('es-CO')}</span></div>
            <div className="flex justify-between"><span className="text-surface-500">Abono Capital:</span><span className="text-emerald-700 font-semibold">${Number(preview.capital).toLocaleString('es-CO')}</span></div>
            <div className="flex justify-between border-t border-surface-200 pt-1"><span className="font-medium">Saldo Nuevo:</span><span className="font-bold">${Number(preview.saldo_nuevo).toLocaleString('es-CO')}</span></div>
          </div>
        )}

        <button onClick={openConfirmModal} disabled={loading || calculandoPreview} className="btn-success w-full py-2.5 text-base">
          {loading ? 'Registrando...' : 'Pagar y Generar Factura'}
        </button>
      </div>

      {modalOpen && confirmPreview && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 animate-fade-in" onClick={() => !loading && setModalOpen(false)}>
          <div className="mx-4 w-full max-w-md rounded-xl bg-white p-6 shadow-premium" onClick={(e) => e.stopPropagation()}>
            <h2 className="mb-4 text-lg font-bold text-surface-900">Confirmar Pago</h2>
            <div className="space-y-1.5 text-sm">
              <div className="flex justify-between"><span className="text-surface-500">Valor a Pagar:</span><span className="font-bold">${Number(form.valor_pagado).toLocaleString('es-CO')}</span></div>
              <div className="flex justify-between"><span className="text-surface-500">Días:</span><span>{confirmPreview.dias_calculados} ({confirmPreview.dias_mora > 0 ? `${confirmPreview.dias_mora} en mora` : 'sin mora'})</span></div>
              <div className="flex justify-between"><span className="text-surface-500">Intereses:</span><span>${Number(confirmPreview.intereses).toLocaleString('es-CO')}</span></div>
              {confirmPreview.tasa_interes_aplicada !== undefined && confirmPreview.tasa_interes_aplicada !== null && (
                <div className="flex justify-between text-surface-400 text-xs"><span>Tasa aplicada:</span><span>{Number(confirmPreview.tasa_interes_aplicada)}%</span></div>
              )}
              {Number(confirmPreview.intereses_mora) > 0 && (
                <div className="flex justify-between text-red-600"><span>Intereses Mora:</span><span>${Number(confirmPreview.intereses_mora).toLocaleString('es-CO')}</span></div>
              )}
              <div className="flex justify-between font-medium border-t border-surface-100 pt-1"><span>Intereses Totales:</span><span>${Number(confirmPreview.intereses_totales).toLocaleString('es-CO')}</span></div>
              <div className="flex justify-between"><span className="text-surface-500">Abono a Capital:</span><span className="text-emerald-700 font-semibold">${Number(confirmPreview.capital).toLocaleString('es-CO')}</span></div>
              <div className="flex justify-between"><span className="text-surface-500">Saldo Anterior:</span><span>${Number(confirmPreview.saldo_anterior).toLocaleString('es-CO')}</span></div>
              <div className="flex justify-between border-t border-surface-100 pt-1"><span className="font-medium">Saldo Nuevo:</span><span className="font-bold">${Number(confirmPreview.saldo_nuevo).toLocaleString('es-CO')}</span></div>
            </div>
            <div className="mt-6 flex gap-3">
              <button onClick={() => setModalOpen(false)} disabled={loading} className="btn-secondary flex-1">Cancelar</button>
              <button onClick={handleConfirmarPago} disabled={loading} className="btn-success flex-1">
                {loading ? 'Procesando...' : 'Confirmar Pago'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function Row({ label, value, bold, danger }: { label: string; value: string; bold?: boolean; danger?: boolean }) {
  return (
    <div className="flex justify-between">
      <span className="text-surface-500">{label}:</span>
      <span className={`${bold ? 'font-bold text-surface-900' : ''} ${danger ? 'text-red-600 font-medium' : ''}`}>{value}</span>
    </div>
  )
}
