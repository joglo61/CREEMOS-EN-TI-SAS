import api from './api'
import type { ApiResponse, TokenResponse, LoginRequest, UserInfo } from '@/types/auth'

export const authService = {
  async login(data: LoginRequest): Promise<ApiResponse<TokenResponse>> {
    const res = await api.post<ApiResponse<TokenResponse>>('/auth/login', data)
    return res.data
  },

  async logout(): Promise<ApiResponse> {
    const res = await api.post<ApiResponse>('/auth/logout')
    return res.data
  },

  async getMe(): Promise<ApiResponse<UserInfo>> {
    const res = await api.get<ApiResponse<UserInfo>>('/auth/me')
    return res.data
  },
}
