import { createContext, useCallback, useEffect, useMemo, useState } from "react"
import { loginRequest, meRequest, refreshRequest, signupRequest } from "@/features/auth/api/auth-api"
import { setupAuthInterceptors } from "@/features/auth/api/auth-http"
import {
  clearTokens,
  getAccessToken,
  setAccessToken,
} from "@/features/auth/lib/token-storage"
import { parseJwtPayload, isExpired } from "@/features/auth/lib/jwt"

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getAccessToken())
  const [userProfile, setUserProfile] = useState(null)
  const [isProfileLoading, setIsProfileLoading] = useState(false)
  const [isBootstrapped, setIsBootstrapped] = useState(false)

  const readUserFromToken = (accessToken) => {
    const payload = parseJwtPayload(accessToken)
    if (!payload?.sub) return null

    return {
      id: payload.sub,
      exp: payload.exp,
    }
  }

  const saveAccessToken = useCallback((accessToken) => {
    setAccessToken(accessToken)
    setToken(accessToken)
  }, [])

  const logout = useCallback((reason = "manual") => {
    clearTokens()
    setToken(null)
    setUserProfile(null)
    setIsProfileLoading(false)
  }, [])

  const login = useCallback(async (email, password) => {
    const data = await loginRequest(email, password)
    saveAccessToken(data.access_token)
    return data
  }, [saveAccessToken])

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
      const data = await meRequest()
      setUserProfile(data)
      return data
    } catch (error) {
      setUserProfile(null)
      const status = error?.response?.status
      const detail = error?.response?.data?.detail || error?.message || "unknown"

      if (status === 401) {
        logout("profile_unauthorized_401")
      }

      throw error
    } finally {
      setIsProfileLoading(false)
    }
  }, [token, logout])

  useEffect(() => {
    const bootstrapAuth = async () => {
      const savedAccessToken = getAccessToken()

      if (savedAccessToken && !isExpired(savedAccessToken, 5_000)) {
        setToken(savedAccessToken)
        setIsBootstrapped(true)
        return
      }

      try {
        const data = await refreshRequest()
        saveAccessToken(data.access_token)
      } catch {
        logout("bootstrap_refresh_failed")
      } finally {
        setIsBootstrapped(true)
      }
    }

    bootstrapAuth()
  }, [logout, saveAccessToken])

  useEffect(() => {
    const teardown = setupAuthInterceptors({
      onAuthFailed: logout,
      onAccessTokenRefreshed: (nextToken) => setToken(nextToken),
    })
    return teardown
  }, [logout])

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
