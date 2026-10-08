import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { clienteService, type ClienteCreateData, type ClienteUpdateData } from '@/services/cliente.service'
import { useUnsaved } from '@/contexts/UnsavedContext'
import { useToast } from '@/contexts/ToastContext'
import CurrencyInput from '@/components/CurrencyInput'

const createSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  cedula: z.string().min(1, 'La cédula es requerida'),
  placa: z.string().min(1, 'La placa es requerida'),
  telefono: z.string().optional(),
  direccion: z.string().optional(),
  correo: z.string().optional(),
  observaciones: z.string().optional(),
  capital_inicial: z.coerce.number().positive('Debe ser mayor a cero'),
  valor_cuota: z.coerce.number().positive('Debe ser mayor a cero'),
  fecha_inicio: z.string().min(1, 'Requerida'),
})

type FormData = z.infer<typeof createSchema>

export default function ClienteFormPage() {
  const { setDirty } = useUnsaved()
  const { addToast } = useToast()
  const { id } = useParams()
  const isEdit = !!id
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const today = new Date().toISOString().split('T')[0]
  const [submitting, setSubmitting] = useState(false)
  const [showHardDeleteModal, setShowHardDeleteModal] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [toggling, setToggling] = useState(false)
  const [clienteEstado, setClienteEstado] = useState('')

  const { register, handleSubmit, reset, control, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(createSchema),
    defaultValues: { fecha_inicio: today },
  })

  useEffect(() => {
    if (isEdit) {
      clienteService.getById(Number(id)).then((res) => {
        if (res.success && res.data) {
          setClienteEstado(res.data.estado)
          reset({
            nombre: res.data.nombre,
            cedula: res.data.cedula,
            placa: res.data.placa,
            telefono: res.data.telefono || '',
            direccion: res.data.direccion || '',
            correo: res.data.correo || '',
            observaciones: res.data.observaciones || '',
            capital_inicial: 0,
            valor_cuota: 0,
            fecha_inicio: '',
          })
        }
      })
    }
  }, [id, isEdit, reset])

  const onSubmit = async (data: FormData) => {
    setSubmitting(true)
    setError('')
    try {
      if (isEdit) {
        const upd: ClienteUpdateData = {
          nombre: data.nombre,
          telefono: data.telefono,
          direccion: data.direccion,
          correo: data.correo,
          observaciones: data.observaciones,
        }
        await clienteService.update(Number(id), upd)
        setDirty()
        addToast('success', 'Cliente actualizado correctamente')
        navigate(`/clientes/${id}`, { replace: true })
      } else {
        const createData: ClienteCreateData = {
          nombre: data.nombre, cedula: data.cedula, placa: data.placa,
          telefono: data.telefono, direccion: data.direccion, correo: data.correo,
          observaciones: data.observaciones, capital_inicial: data.capital_inicial,
          valor_cuota: data.valor_cuota, fecha_inicio: data.fecha_inicio,
        }
        await clienteService.create(createData)
        setDirty()
        addToast('success', 'Cliente creado correctamente')
        navigate('/clientes', { replace: true })
      }
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } }
        setError(axiosErr.response?.data?.detail || 'Error al guardar')
      } else {
        setError('Error de conexión')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="p-6 lg:p-8 max-w-2xl mx-auto animate-fade-in">
      <button onClick={() => navigate(-1)} className="mb-4 text-sm text-primary-600 hover:text-primary-700 font-medium">&larr; Volver</button>
      <h1 className="page-title mb-6">{isEdit ? 'Editar Cliente' : 'Nuevo Cliente'}</h1>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 card p-6">
        {error && <div className="rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">{error}</div>}

        <div>
          <h3 className="section-label mb-3">Información Personal</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-surface-700 mb-1">Nombre *</label>
              <input type="text" {...register('nombre')} className="input" />
              {errors.nombre && <p className="mt-1 text-xs text-red-600">{errors.nombre.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-surface-700 mb-1">Cédula *</label>
              <input type="text" {...register('cedula')} disabled={isEdit} className="input disabled:bg-surface-50 disabled:text-surface-400" />
              {errors.cedula && <p className="mt-1 text-xs text-red-600">{errors.cedula.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-surface-700 mb-1">Placa *</label>
              <input type="text" {...register('placa')} disabled={isEdit} className="input disabled:bg-surface-50 disabled:text-surface-400" />
              {errors.placa && <p className="mt-1 text-xs text-red-600">{errors.placa.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-surface-700 mb-1">Teléfono</label>
              <input type="text" {...register('telefono')} className="input" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-surface-700 mb-1">Dirección</label>
              <input type="text" {...register('direccion')} className="input" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-surface-700 mb-1">Correo</label>
              <input type="email" {...register('correo')} className="input" />
            </div>
          </div>
        </div>

        {!isEdit && (
          <div>
            <h3 className="section-label mb-3">Información del Préstamo</h3>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-surface-700 mb-1">Valor del Préstamo *</label>
                <Controller
                  name="capital_inicial"
                  control={control}
                  render={({ field }) => (
                    <CurrencyInput value={field.value} onChange={field.onChange} className="input" />
                  )}
                />
                {errors.capital_inicial && <p className="mt-1 text-xs text-red-600">{errors.capital_inicial.message}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-surface-700 mb-1">Valor de la Cuota *</label>
                <Controller
                  name="valor_cuota"
                  control={control}
                  render={({ field }) => (
                    <CurrencyInput value={field.value} onChange={field.onChange} className="input" />
                  )}
                />
                {errors.valor_cuota && <p className="mt-1 text-xs text-red-600">{errors.valor_cuota.message}</p>}
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-surface-700 mb-1">Fecha de Inicio *</label>
                <input type="date" {...register('fecha_inicio')} className="input" />
                {errors.fecha_inicio && <p className="mt-1 text-xs text-red-600">{errors.fecha_inicio.message}</p>}
                <p className="mt-1 text-xs text-surface-400">El primer pago se calculará automáticamente un mes después.</p>
              </div>
            </div>
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1">Observaciones</label>
          <textarea rows={3} {...register('observaciones')} className="input" />
        </div>

        <div className="flex flex-wrap justify-between gap-3 pt-2 border-t border-surface-100">
          <div className="flex gap-2">
            {isEdit && (
              <>
                <button type="button" onClick={async () => {
                  setToggling(true); setError('')
                  try {
                    const res = await clienteService.toggleEstado(Number(id))
                    setClienteEstado(res.data?.estado || '')
                    addToast('success', `Cliente ${res.data?.estado === 'ACTIVO' ? 'activado' : 'desactivado'}`)
                  } catch {
                    setError('Error al cambiar estado')
                  } finally { setToggling(false) }
                }} disabled={toggling}
                  className={`btn-sm ${clienteEstado === 'ACTIVO' ? 'btn-ghost text-amber-600' : 'btn-ghost text-emerald-600'}`}>
                  {toggling ? '...' : clienteEstado === 'ACTIVO' ? 'Desactivar' : 'Activar'}
                </button>
                <button type="button" onClick={() => setShowHardDeleteModal(true)} className="btn-sm btn-ghost text-red-600">Eliminar</button>
              </>
            )}
          </div>
          <div className="flex gap-2">
            <button type="button" onClick={() => navigate(-1)} className="btn-secondary">Cancelar</button>
            <button type="submit" disabled={submitting} className="btn-primary">
              {submitting ? 'Guardando...' : isEdit ? 'Actualizar' : 'Crear Cliente'}
            </button>
          </div>
        </div>
      </form>

      {showHardDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 animate-fade-in" onClick={() => setShowHardDeleteModal(false)}>
          <div className="w-full max-w-sm rounded-xl bg-white p-6 shadow-premium mx-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-surface-900">¿Eliminar permanentemente?</h3>
            <p className="mt-2 text-sm text-surface-500">
              Esta acción eliminará el cliente y todos sus préstamos, pagos y facturas asociados. <strong className="text-red-600">No se puede deshacer.</strong>
            </p>
            <div className="mt-6 flex justify-end gap-3">
              <button type="button" onClick={() => setShowHardDeleteModal(false)} className="btn-secondary">Cancelar</button>
              <button type="button" onClick={async () => {
                setDeleting(true)
                try {
                  await clienteService.hardDelete(Number(id))
                  addToast('success', 'Cliente eliminado permanentemente')
                  navigate('/clientes', { replace: true })
                } catch {
                  setError('Error al eliminar')
                  setShowHardDeleteModal(false)
                } finally { setDeleting(false) }
              }} disabled={deleting} className="btn-danger">
                {deleting ? 'Eliminando...' : 'Sí, eliminar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
