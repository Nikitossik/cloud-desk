import { createContext, useCallback, useEffect, useMemo, useState } from "react"
import { loginRequest, refreshRequest, signupRequest } from "@/features/auth/api/auth-api"
import { setupAuthInterceptors } from "@/features/auth/api/auth-http"
import {
  clearTokens,
  getAccessToken,
  setAccessToken,
} from "@/features/auth/lib/token-storage"
import { parseJwtPayload, isExpired } from "@/features/auth/lib/jwt"
import { queryClient } from "@/shared/lib/query-client"

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getAccessToken())
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
    void reason
    clearTokens()
    queryClient.clear()
    setToken(null)
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

  const user = useMemo(() => readUserFromToken(token), [token])

  const value = useMemo(
    () => ({
      user,
      token,
      isBootstrapped,
      isAuthenticated: Boolean(token),
      login,
      signup,
      setAuthToken: saveAccessToken,
      logout,
    }),
    [
      user,
      token,
      isBootstrapped,
      login,
      signup,
      saveAccessToken,
      logout,
    ]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
