import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  type: ToastType
  title: string
  message?: string
}

interface ToastContextValue {
  toasts: Toast[]
  addToast: (type: ToastType, title: string, message?: string) => void
  removeToast: (id: number) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

let nextId = 1

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const removeToast = useCallback((id: number) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const addToast = useCallback((type: ToastType, title: string, message?: string) => {
    const id = nextId++
    setToasts(prev => [...prev, { id, type, title, message }])
    setTimeout(() => removeToast(id), 5000)
  }, [removeToast])

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}

const typeStyles: Record<ToastType, { bg: string; border: string; icon: string }> = {
  success: { bg: 'bg-green-50', border: 'border-green-400', icon: '✓' },
  error: { bg: 'bg-red-50', border: 'border-red-400', icon: '✕' },
  warning: { bg: 'bg-yellow-50', border: 'border-yellow-400', icon: '⚠' },
  info: { bg: 'bg-primary-50', border: 'border-primary-400', icon: 'ℹ' },
}

function ToastContainer({ toasts, onClose }: { toasts: Toast[]; onClose: (id: number) => void }) {
  if (toasts.length === 0) return null
  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {toasts.map(t => {
        const s = typeStyles[t.type]
        return (
          <div key={t.id} className={`${s.bg} ${s.border} border-l-4 rounded shadow-lg p-3 flex items-start gap-2 animate-slide-in`}>
            <span className="font-bold text-lg leading-none mt-0.5">{s.icon}</span>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-sm text-surface-900">{t.title}</p>
              {t.message && <p className="text-xs text-surface-600 mt-0.5">{t.message}</p>}
            </div>
            <button onClick={() => onClose(t.id)} className="text-surface-400 hover:text-surface-600 text-sm leading-none">&times;</button>
          </div>
        )
      })}
    </div>
  )
}
