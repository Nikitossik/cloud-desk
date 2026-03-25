import { http } from "@/shared/api/http-client"
import { refreshRequest } from "@/features/auth/api/auth-api"
import {
  clearTokens,
  getAccessToken,
  setAccessToken,
} from "@/features/auth/lib/token-storage"
import { isExpired } from "@/features/auth/lib/jwt"
import { getOrCreateDeviceFingerprint } from "@/features/device/lib/fingerprint"

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

  refreshPromise = refreshRequest()
    .then((data) => {
      setAccessToken(data.access_token)
      onAccessTokenRefreshed?.(data.access_token)
      return data.access_token
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
    const deviceFingerprint = getOrCreateDeviceFingerprint()
    config.headers = config.headers ?? {}
    if (deviceFingerprint) {
      config.headers["X-Device-Fingerprint"] = deviceFingerprint
    }

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
        onAuthFailed?.("refresh_failed")
        throw error
      }
    }

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
        onAuthFailed?.("refresh_failed_after_401")
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
