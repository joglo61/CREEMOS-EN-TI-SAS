export interface LoginRequest {
  usuario: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  usuario: string
  nombre: string
  rol: string
}

export interface UserInfo {
  id: number
  usuario: string
  nombre: string
  rol: string
  activo: boolean
}

export interface ApiResponse<T = unknown> {
  success: boolean
  message?: string
  data?: T
}
