import { createContext, useEffect, useMemo, useRef, useState } from "react"
import { loginRequest, signupRequest } from "@/features/auth/api/auth-api"
import { setupAuthInterceptors } from "@/features/auth/api/auth-http"
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokenPair,
} from "@/features/auth/lib/token-storage"
import { getExpMs, parseJwtPayload, isExpired } from "@/features/auth/lib/jwt"

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getAccessToken())
  const [isBootstrapped, setIsBootstrapped] = useState(false)
  const refreshExpiryTimerRef = useRef(null)

  const readUserFromToken = (accessToken) => {
    const payload = parseJwtPayload(accessToken)
    if (!payload?.sub) return null

    return {
      id: payload.sub,
      exp: payload.exp,
    }
  }

  const saveTokenPair = (accessToken, refreshToken) => {
    setTokenPair({
      access_token: accessToken,
      refresh_token: refreshToken,
    })
    setToken(accessToken)
  }

  const logout = () => {
    clearTokens()
    setToken(null)
  }

  const login = async (email, password) => {
    const data = await loginRequest(email, password)
    saveTokenPair(data.access_token, data.refresh_token)
    return data
  }

  const signup = async ({ name, surname, email, password }) => {
    await signupRequest({ name, surname, email, password })
    return login(email, password)
  }

  useEffect(() => {
    const savedRefreshToken = getRefreshToken()

    if (!savedRefreshToken || isExpired(savedRefreshToken, 5_000)) {
      logout()
      setIsBootstrapped(true)
      return
    }

    const savedAccessToken = getAccessToken()
    if (savedAccessToken) {
      setToken(savedAccessToken)
    }

    setIsBootstrapped(true)
  }, [])

  useEffect(() => {
    const teardown = setupAuthInterceptors({ onAuthFailed: logout })
    return teardown
  }, [token])

  useEffect(() => {
    if (refreshExpiryTimerRef.current) {
      clearTimeout(refreshExpiryTimerRef.current)
      refreshExpiryTimerRef.current = null
    }

    const refreshToken = getRefreshToken()
    if (!refreshToken) {
      return
    }

    const expMs = getExpMs(refreshToken)
    if (!expMs) {
      logout()
      return
    }

    const delay = expMs - Date.now()
    if (delay <= 0) {
      logout()
      return
    }

    refreshExpiryTimerRef.current = setTimeout(() => {
      logout()
    }, delay)

    return () => {
      if (refreshExpiryTimerRef.current) {
        clearTimeout(refreshExpiryTimerRef.current)
        refreshExpiryTimerRef.current = null
      }
    }
  }, [token])

  const user = useMemo(() => readUserFromToken(token), [token])

  const value = useMemo(
    () => ({
      user,
      token,
      isBootstrapped,
      isAuthenticated: Boolean(token),
      login,
      signup,
      logout,
    }),
    [user, token, isBootstrapped]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
