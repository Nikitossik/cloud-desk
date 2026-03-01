import { http } from "@/shared/api/http-client"
import { refreshRequest } from "@/features/auth/api/auth-api"
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokenPair,
} from "@/features/auth/lib/token-storage"
import { isExpired } from "@/features/auth/lib/jwt"

let requestInterceptorId = null
let responseInterceptorId = null
let refreshPromise = null

function shouldSkipAuthAttach(config) {
  return Boolean(config?.skipAuthAttach)
}

function shouldSkipAuthRefresh(config) {
  return Boolean(config?.skipAuthRefresh)
}

function refreshSingleFlight(onAccessTokenRefreshed) {
  if (refreshPromise) {
    return refreshPromise
  }

  const refreshToken = getRefreshToken()
  if (!refreshToken || isExpired(refreshToken, 5_000)) {
    return Promise.reject(new Error("Refresh token is missing or expired"))
  }

  refreshPromise = refreshRequest(refreshToken)
    .then((pair) => {
      setTokenPair(pair)
      onAccessTokenRefreshed?.(pair.access_token)
      return pair.access_token
    })
    .finally(() => {
      refreshPromise = null
    })

  return refreshPromise
}

export function setupAuthInterceptors({ onAuthFailed, onAccessTokenRefreshed }) {
  if (requestInterceptorId !== null) {
    http.interceptors.request.eject(requestInterceptorId)
    requestInterceptorId = null
  }

  if (responseInterceptorId !== null) {
    http.interceptors.response.eject(responseInterceptorId)
    responseInterceptorId = null
  }

  requestInterceptorId = http.interceptors.request.use(async (config) => {
    if (shouldSkipAuthAttach(config)) {
      return config
    }

    let accessToken = getAccessToken()
    if (!accessToken) {
      return config
    }

    if (isExpired(accessToken, 5_000)) {
      try {
        accessToken = await refreshSingleFlight(onAccessTokenRefreshed)
      } catch (error) {
        clearTokens()
        onAuthFailed?.()
        throw error
      }
    }

    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${accessToken}`
    return config
  })

  responseInterceptorId = http.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error?.config
      const statusCode = error?.response?.status

      if (!originalRequest) {
        return Promise.reject(error)
      }

      const canRetry =
        !originalRequest._retry && !shouldSkipAuthRefresh(originalRequest)

      if (statusCode !== 401 || !canRetry) {
        return Promise.reject(error)
      }

      originalRequest._retry = true

      try {
        const newAccessToken = await refreshSingleFlight(onAccessTokenRefreshed)
        originalRequest.headers = originalRequest.headers ?? {}
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return http(originalRequest)
      } catch (refreshError) {
        clearTokens()
        onAuthFailed?.()
        return Promise.reject(refreshError)
      }
    }
  )

  return () => {
    if (requestInterceptorId !== null) {
      http.interceptors.request.eject(requestInterceptorId)
      requestInterceptorId = null
    }

    if (responseInterceptorId !== null) {
      http.interceptors.response.eject(responseInterceptorId)
      responseInterceptorId = null
    }
  }
}
