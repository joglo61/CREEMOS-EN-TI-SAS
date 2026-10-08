import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

function _fmtDetail(d: unknown): string {
  if (typeof d === 'string') return d
  if (Array.isArray(d)) return d.map((e) => e.msg ?? JSON.stringify(e)).join('; ')
  if (d && typeof d === 'object') return JSON.stringify(d)
  return 'Error desconocido.'
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    if (error.response?.data?.detail) {
      error.response.data.detail = _fmtDetail(error.response.data.detail)
    }
    return Promise.reject(error)
  },
)

export default api
