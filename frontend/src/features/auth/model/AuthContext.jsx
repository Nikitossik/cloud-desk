import { createContext, useCallback, useEffect, useMemo, useRef, useState } from "react"
import { loginRequest, meRequest, signupRequest } from "@/features/auth/api/auth-api"
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
  const [userProfile, setUserProfile] = useState(null)
  const [isProfileLoading, setIsProfileLoading] = useState(false)
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

  const saveTokenPair = useCallback((accessToken, refreshToken) => {
    setTokenPair({
      access_token: accessToken,
      refresh_token: refreshToken,
    })
    setToken(accessToken)
  }, [])

  const logout = useCallback(() => {
    clearTokens()
    setToken(null)
    setUserProfile(null)
    setIsProfileLoading(false)
  }, [])

  const login = useCallback(async (email, password) => {
    const data = await loginRequest(email, password)
    saveTokenPair(data.access_token, data.refresh_token)
    return data
  }, [saveTokenPair])

  const signup = useCallback(async ({ name, surname, email, password }) => {
    await signupRequest({ name, surname, email, password })
    return login(email, password)
  }, [login])

  const refreshUserProfile = useCallback(async () => {
    if (!token) {
      setUserProfile(null)
      setIsProfileLoading(false)
      return null
    }

    setIsProfileLoading(true)

    try {
      const data = await meRequest(token)
      setUserProfile(data)
      return data
    } catch (error) {
      setUserProfile(null)
      throw error
    } finally {
      setIsProfileLoading(false)
    }
  }, [token])

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
  }, [logout])

  useEffect(() => {
    const teardown = setupAuthInterceptors({
      onAuthFailed: logout,
      onAccessTokenRefreshed: (nextToken) => setToken(nextToken),
    })
    return teardown
  }, [logout])

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
  }, [token, logout])

  useEffect(() => {
    if (!token) {
      setUserProfile(null)
      setIsProfileLoading(false)
      return
    }

    const loadProfile = async () => {
      try {
        await refreshUserProfile()
      } catch {
        return
      }
    }

    loadProfile()
  }, [token, refreshUserProfile])

  const user = useMemo(() => readUserFromToken(token), [token])

  const value = useMemo(
    () => ({
      user,
      userProfile,
      isProfileLoading,
      token,
      isBootstrapped,
      isAuthenticated: Boolean(token),
      login,
      signup,
      refreshUserProfile,
      logout,
    }),
    [
      user,
      userProfile,
      isProfileLoading,
      token,
      isBootstrapped,
      login,
      signup,
      refreshUserProfile,
      logout,
    ]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
