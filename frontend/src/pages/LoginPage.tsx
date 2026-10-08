import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/contexts/AuthContext'
import { useToast } from '@/contexts/ToastContext'
import { authService } from '@/services/auth.service'
import type { LoginRequest } from '@/types/auth'

const loginSchema = z.object({
  usuario: z.string().min(1, 'El usuario es requerido'),
  password: z.string().min(1, 'La contraseña es requerida'),
})

export default function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const { addToast } = useToast()
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginRequest) => {
    setSubmitting(true)
    setError('')
    try {
      const res = await authService.login(data)
      if (res.success && res.data) {
        login(res.data.access_token, {
          id: 0,
          usuario: res.data.usuario,
          nombre: res.data.nombre,
          rol: res.data.rol,
          activo: true,
        })
        addToast('success', `Bienvenido, ${res.data.nombre}`)
        navigate('/', { replace: true })
      }
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { message?: string; detail?: string } } }
        setError(axiosErr.response?.data?.detail || axiosErr.response?.data?.message || 'Credenciales inválidas')
      } else {
        setError('Error de conexión')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary-900 to-primary-700 px-4">
      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-premium">
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-600 to-primary-800 text-base font-bold text-white shadow-sm" aria-hidden="true">CT</div>
          <h1 className="text-2xl font-bold tracking-tight text-surface-900">CREEMOS EN TI SAS</h1>
          <p className="mt-1 text-sm text-surface-500">Sistema de Administración de Préstamos</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label htmlFor="login-usuario" className="mb-1 block text-sm font-medium text-surface-700">Usuario</label>
            <input
              id="login-usuario"
              type="text"
              autoFocus
              autoComplete="username"
              {...register('usuario')}
              className="input"
            />
            {errors.usuario && (
              <p className="mt-1 text-xs text-red-600">{errors.usuario.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="login-password" className="mb-1 block text-sm font-medium text-surface-700">Contraseña</label>
            <div className="relative">
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                {...register('password')}
                className="input pr-20"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-1 top-1/2 -translate-y-1/2 rounded-md px-2 py-1 text-sm text-surface-500 hover:text-surface-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
                aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
              >
                {showPassword ? 'Ocultar' : 'Mostrar'}
              </button>
            </div>
            {errors.password && (
              <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>
            )}
          </div>

          {error && (
            <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="btn-primary w-full py-2.5 text-base"
          >
            {submitting ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </div>
    </div>
  )
}
