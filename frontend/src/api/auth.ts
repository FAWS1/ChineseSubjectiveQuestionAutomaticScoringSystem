import axios from 'axios'

interface LoginData {
  username: string
  password: string
  role: 'teacher' | 'student'
}

interface RegisterData extends LoginData {
  email?: string
  phone?: string
}

interface AuthResponse {
  token: string
  user: {
    id: number
    username: string
    role: string
  }
}

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理token过期
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const login = async (data: LoginData): Promise<AuthResponse> => {
  const response = await api.post('/login/', data)
  return response.data
}

export const register = async (data: RegisterData): Promise<AuthResponse> => {
  const response = await api.post('/register/', data)
  return response.data
}

export const checkAuth = async (): Promise<boolean> => {
  try {
    await api.get('/check-auth/')
    return true
  } catch {
    return false
  }
}