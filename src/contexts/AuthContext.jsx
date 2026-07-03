import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const AuthContext = createContext(null)

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' },
})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token')
    if (storedToken) {
      api.defaults.headers.common.Authorization = `Bearer ${storedToken}`
      api.get('/auth/me')
        .then((response) => setUser(response.data.user))
        .catch(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          setToken(null)
          setUser(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (payload) => {
    const response = await api.post('/auth/login', payload)
    const { access_token, refresh_token, user: authUser } = response.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    api.defaults.headers.common.Authorization = `Bearer ${access_token}`
    setToken(access_token)
    setUser(authUser)
    navigate('/dashboard')
    return response.data
  }

  const register = async (payload) => {
    const response = await api.post('/auth/register', payload)
    return response.data
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete api.defaults.headers.common.Authorization
      setToken(null)
      setUser(null)
      navigate('/auth')
    }
  }

  const value = useMemo(() => ({ user, token, loading, login, register, logout, api }), [user, token, loading, login, register, logout])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
