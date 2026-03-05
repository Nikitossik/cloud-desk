import { useState } from "react"
import { Navigate, useNavigate } from "react-router"
import { useMutation } from "@tanstack/react-query"

import { useAuth } from "@/features/auth/hooks/use-auth"
import {
  extractResolutionToken,
  isResolutionTokenProblem,
} from "@/features/auth/lib/resolution-token"
import {
  cancelDeviceResolutionRequest,
  getResolutionDevicesRequest,
  resolveDeviceCreateRequest,
  resolveDeviceRebindRequest,
} from "@/features/auth/api/auth-api"
import { ensureDeviceFingerprint, regenerateDeviceFingerprint } from "@/features/device/lib/fingerprint"
import { detectLocalDeviceRequest } from "@/features/device/api/device-api"
import {
  CURRENT_DEVICE_QUERY_KEY,
  USER_DEVICES_QUERY_KEY,
} from "@/features/device/lib/query-keys"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
import { queryClient } from "@/shared/lib/query-client"
import { Button } from "@/components/ui/button"
import { AuthCredentialsForm } from "@/features/auth/components/auth-credentials-form"
import { DeviceResolutionDialog } from "@/features/auth/components/device-resolution-dialog"

export function AuthPage() {
  const navigate = useNavigate()
  const { isAuthenticated, login, signup, setAuthToken } = useAuth()

  const [mode, setMode] = useState("login")
  const [authErrorMessage, setAuthErrorMessage] = useState("")
  const [resolutionError, setResolutionError] = useState("")
  const [isResolutionModalOpen, setIsResolutionModalOpen] = useState(false)
  const [resolutionMode, setResolutionMode] = useState("login")
  const [resolutionToken, setResolutionToken] = useState("")
  const [resolutionDevices, setResolutionDevices] = useState([])
  const [localDeviceInfo, setLocalDeviceInfo] = useState(null)
  const [allowAutoRedirect, setAllowAutoRedirect] = useState(true)

  const authMutation = useMutation({
    mutationFn: async (values) => {
      setAuthErrorMessage("")
      setResolutionError("")

      try {
        if (mode === "signup") {
          ensureDeviceFingerprint()
          await signup({
            name: values.name,
            surname: values.surname,
            email: values.email,
            password: values.password,
          })
          navigate("/", { replace: true })
          return
        }

        await login(values.email, values.password)
        navigate("/", { replace: true })
      } catch (error) {
        const nextResolutionToken = extractResolutionToken(error)

        if (!nextResolutionToken) {
          throw error
        }

        try {
          const localDevice = await detectLocalDeviceRequest()
          const devices =
            mode === "login" ? await getResolutionDevicesRequest(nextResolutionToken) : []

          setResolutionToken(nextResolutionToken)
          setResolutionDevices(devices)
          setLocalDeviceInfo(localDevice)
          setResolutionMode(mode)
          setIsResolutionModalOpen(true)
          setAllowAutoRedirect(false)
        } catch (resolutionError) {
          if (isResolutionTokenProblem(resolutionError)) {
            setResolutionError("")
            setResolutionToken("")
            setResolutionDevices([])
            setLocalDeviceInfo(null)
            setResolutionMode("login")
            setIsResolutionModalOpen(false)
            setAllowAutoRedirect(true)
            setAuthErrorMessage("Device verification session expired. Please try again.")
            return
          }

          throw resolutionError
        }
      }
    },
  })

  const resolutionMutation = useMutation({
    mutationFn: async (payload) => {
      const nextFingerprint = regenerateDeviceFingerprint()

      if (!resolutionToken) {
        throw new Error("Resolution token is missing")
      }

      if (payload.action === "rebind") {
        const data = await resolveDeviceRebindRequest({
          resolutionToken,
          targetDeviceId: payload.targetDeviceId,
          newFingerprint: nextFingerprint,
        })
        setAuthToken(data.access_token)
        return
      }

      const data = await resolveDeviceCreateRequest({
        resolutionToken,
        newFingerprint: nextFingerprint,
        displayName: payload.displayName,
      })
      setAuthToken(data.access_token)
    },
  })

  const cancelResolutionMutation = useMutation({
    mutationFn: async ({ token, mode }) => {
      if (!token) return

      await cancelDeviceResolutionRequest({
        resolutionToken: token,
        removeUser: mode === "signup",
      })
    },
  })

  if (isAuthenticated && allowAutoRedirect && !isResolutionModalOpen) {
    return <Navigate to="/" replace />
  }

  const isLoading = authMutation.isPending || resolutionMutation.isPending
  const errorMessage =
    authErrorMessage ||
    authMutation.error?.response?.data?.detail ||
    authMutation.error?.message

  const handleAuthSubmit = (values) => {
    setAuthErrorMessage("")
    setAllowAutoRedirect(true)
    authMutation.mutate(values)
  }

  const handleResolutionTokenProblem = () => {
    setResolutionError("")
    setResolutionToken("")
    setResolutionDevices([])
    setLocalDeviceInfo(null)
    setResolutionMode("login")
    setIsResolutionModalOpen(false)
    setAllowAutoRedirect(true)
    setAuthErrorMessage("Device verification session expired. Please try again.")
  }

  const handleResolutionSubmit = (payload) => {
    setResolutionError("")
    resolutionMutation.mutate(payload, {
      onSuccess: async () => {
        await Promise.all([
          queryClient.invalidateQueries({ queryKey: CURRENT_DEVICE_QUERY_KEY }),
          queryClient.invalidateQueries({ queryKey: USER_DEVICES_QUERY_KEY }),
          queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY }),
        ])

        setIsResolutionModalOpen(false)
        setAllowAutoRedirect(true)
        navigate("/", { replace: true })
      },
      onError: (error) => {
        if (isResolutionTokenProblem(error)) {
          handleResolutionTokenProblem()
          return
        }

        const message =
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to resolve device"
        setResolutionError(String(message))
      },
    })
  }

  const resetResolutionState = () => {
    setResolutionError("")
    setResolutionToken("")
    setResolutionDevices([])
    setLocalDeviceInfo(null)
    setResolutionMode("login")
    setIsResolutionModalOpen(false)
    setAllowAutoRedirect(false)
  }

  const handleResolutionCancel = () => {
    cancelResolutionMutation.mutate(
      {
        token: resolutionToken,
        mode: resolutionMode,
      },
      {
        onSuccess: () => {
          resetResolutionState()
        },
        onError: (error) => {
          if (isResolutionTokenProblem(error)) {
            handleResolutionTokenProblem()
            return
          }

          const message =
            error?.response?.data?.detail ||
            error?.message ||
            "Failed to cancel device verification"
          setResolutionError(String(message))
        },
      }
    )
  }

  const switchMode = (nextMode) => {
    setMode(nextMode)
    setAuthErrorMessage("")
    authMutation.reset()
    resetResolutionState()
    setAllowAutoRedirect(true)
  }

  return (
    <div className="flex min-h-svh items-center justify-center p-4">
      <div className="bg-card text-card-foreground w-full max-w-md rounded-xl border p-6">
        <div className="mb-6 space-y-1">
          <h1 className="text-2xl font-semibold">Cloud Desk</h1>
          <p className="text-muted-foreground text-sm">
            {mode === "login" ? "Log in to continue" : "Create a new account"}
          </p>
        </div>

        <div className="mb-4 grid grid-cols-2 gap-2">
          <Button
            type="button"
            variant={mode === "login" ? "default" : "outline"}
            onClick={() => switchMode("login")}
            disabled={isLoading}
          >
            Login
          </Button>
          <Button
            type="button"
            variant={mode === "signup" ? "default" : "outline"}
            onClick={() => switchMode("signup")}
            disabled={isLoading}
          >
            Sign up
          </Button>
        </div>

        <AuthCredentialsForm
          mode={mode}
          isLoading={isLoading}
          errorMessage={errorMessage}
          onSubmitValues={handleAuthSubmit}
        />

        <DeviceResolutionDialog
          open={isResolutionModalOpen}
          mode={resolutionMode}
          devices={resolutionDevices}
          currentDeviceInfo={localDeviceInfo}
          isLoading={resolutionMutation.isPending || cancelResolutionMutation.isPending}
          errorMessage={resolutionError}
          onSubmitResolution={handleResolutionSubmit}
          onCancelResolution={handleResolutionCancel}
        />
      </div>
    </div>
  )
}
