import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import type { UserInfo } from '@/types/auth'
import { authService } from '@/services/auth.service'

interface AuthContextType {
  user: UserInfo | null
  token: string | null
  isAuthenticated: boolean
  login: (token: string, user: UserInfo) => void
  logout: () => Promise<void>
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserInfo | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (token) {
      authService.getMe()
        .then((res) => {
          if (res.data) {
            setUser(res.data)
          }
        })
        .catch(() => {
          localStorage.removeItem('access_token')
          setToken(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [token])

  const login = (newToken: string, userInfo: UserInfo) => {
    localStorage.setItem('access_token', newToken)
    setToken(newToken)
    setUser(userInfo)
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch {
      // ignore
    }
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
