import { useEffect, useState } from 'react'
import { Navigate, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { useUnsaved } from '@/contexts/UnsavedContext'

const menuItems = [
  { label: 'Dashboard', path: '/', icon: 'layout-dashboard' },
  { label: 'Clientes', path: '/clientes', icon: 'users' },
  { label: 'Pago de la Cuota', path: '/prestamos', icon: 'coins' },
  { label: 'Facturas', path: '/facturas', icon: 'receipt' },
  { label: 'Reportes', path: '/reportes', icon: 'chart-bar' },
  { label: 'Excel', path: '/excel', icon: 'file-spreadsheet' },
  { label: 'Sync', path: '/sync', icon: 'refresh' },
  { label: 'Usuarios', path: '/usuarios', icon: 'user-cog', adminOnly: true },
  { label: 'Backups', path: '/backups', icon: 'database', adminOnly: true },
  { label: 'Config', path: '/config', icon: 'settings', adminOnly: true },
]

const iconPaths: Record<string, string> = {
  'layout-dashboard': 'M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z',
  'users': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
  'coins': 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
  'receipt': 'M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2z',
  'chart-bar': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
  'file-spreadsheet': 'M9 17h6m-2-4h-2m-4-7h6m4 12V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2z',
  'refresh': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
  'user-cog': 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
  'database': 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4',
  'settings': 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
}

export default function ProtectedLayout() {
  const { isAuthenticated, loading, user, logout } = useAuth()
  const { isDirty, markClean } = useUnsaved()
  const navigate = useNavigate()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (isDirty) e.preventDefault()
    }
    window.addEventListener('beforeunload', handler)
    return () => window.removeEventListener('beforeunload', handler)
  }, [isDirty])

  const handleLogout = () => {
    if (isDirty) {
      const ok = window.confirm('Hay datos sin guardar en Excel. ¿Estás seguro de cerrar sesión?')
      if (!ok) return
    }
    markClean()
    logout()
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gradient-to-br from-primary-950 via-primary-900 to-surface-900">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-white/20 border-t-white" />
          <p className="text-sm font-medium text-white/60">Cargando...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  const isActive = (path: string) =>
    path === '/' ? location.pathname === '/' : location.pathname.startsWith(path)

  return (
    <div className="flex h-screen overflow-hidden bg-surface-50">
      <aside className={`flex flex-col bg-white border-r border-surface-200 transition-all duration-300 ${sidebarOpen ? 'w-60' : 'w-0 -ml-60'} lg:w-60 lg:ml-0`}>
        <div className="flex items-center gap-3 border-b border-surface-100 px-5 py-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary-600 to-primary-800 text-white text-sm font-bold shadow-sm">
            CT
          </div>
          <div className="leading-tight">
            <p className="text-sm font-bold text-surface-900">Creemos en Ti</p>
            <p className="text-[10px] font-medium text-surface-400 uppercase tracking-wider">Préstamos</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto scrollbar-thin px-2 py-3">
          <nav className="space-y-0.5" aria-label="Menú principal">
            {menuItems.filter((item) => !('adminOnly' in item) || user?.rol === 'ADMINISTRADOR').map((item) => {
              const active = isActive(item.path)
              return (
                <button
                  key={item.path}
                  onClick={() => navigate(item.path)}
                  aria-current={active ? 'page' : undefined}
                  className={`group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150 ${
                    active
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-surface-500 hover:bg-surface-100 hover:text-surface-700'
                  }`}
                >
                  <svg className={`h-5 w-5 shrink-0 transition-colors ${active ? 'text-primary-600' : 'text-surface-400 group-hover:text-surface-500'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d={iconPaths[item.icon]} />
                  </svg>
                  <span>{item.label}</span>
                  {active && <span className="ml-auto h-2 w-2 rounded-full bg-primary-500" />}
                </button>
              )
            })}
          </nav>
        </div>

        <div className="border-t border-surface-100 p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary-500 to-primary-700 text-white text-xs font-bold shadow-sm">
              {user?.nombre?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div className="min-w-0 flex-1 leading-tight">
              <p className="truncate text-sm font-semibold text-surface-800">{user?.nombre}</p>
              <p className="text-xs font-medium text-surface-400">{user?.rol}</p>
            </div>
          </div>
        </div>
      </aside>

      <div className="flex flex-1 flex-col min-w-0">
        <header className="flex items-center justify-end gap-4 border-b border-surface-200 bg-white/80 backdrop-blur-md px-6 py-3">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="btn-ghost p-1.5 lg:hidden" aria-label="Abrir o cerrar menú">
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          </button>
          <div className="flex items-center gap-3 ml-auto">
            {isDirty && (
              <span className="flex items-center gap-1.5 rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
                <span className="inline-block h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse" />
                Sin guardar
              </span>
            )}
            <button
              onClick={handleLogout}
              className="btn-ghost btn-sm text-surface-500 hover:text-red-600"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
              </svg>
              Salir
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto scrollbar-thin">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
