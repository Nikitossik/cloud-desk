import { useState } from "react"
import { Navigate, useNavigate } from "react-router"
import { useMutation } from "react-query"

import { useAuth } from "@/features/auth/hooks/use-auth"
import { ensureDeviceFingerprint } from "@/features/device/lib/fingerprint"
import { useResolveDeviceAfterAuth } from "@/features/device/hooks/use-resolve-device-after-auth"
import { useUpdateCurrentDeviceMutation } from "@/features/device/hooks/use-update-current-device-mutation"
import { Button } from "@/components/ui/button"
import { AuthCredentialsForm } from "@/features/auth/components/auth-credentials-form"
import { DetectedDeviceDialog } from "@/features/auth/components/detected-device-dialog"

export function AuthPage() {
  const navigate = useNavigate()
  const { isAuthenticated, login, signup, logout } = useAuth()
  const resolveDeviceAfterAuth = useResolveDeviceAfterAuth()

  const [mode, setMode] = useState("login")
  const [deviceName, setDeviceName] = useState("")
  const [deviceStepError, setDeviceStepError] = useState("")
  const [authErrorMessage, setAuthErrorMessage] = useState("")
  const [isDeviceModalOpen, setIsDeviceModalOpen] = useState(false)
  const [detectedDevice, setDetectedDevice] = useState(null)
  const [allowAutoRedirect, setAllowAutoRedirect] = useState(true)

  const authMutation = useMutation(async (values) => {
    setAuthErrorMessage("")
    setDeviceStepError("")

    if (mode === "login") {
      await login(values.email, values.password)
      const result = await resolveDeviceAfterAuth()

      if (result.wasKnown) {
        navigate("/", { replace: true })
        return
      }

      logout("login_device_not_found")
      setAuthErrorMessage("Device not found for this fingerprint. Bind/create flow will be added next.")
      return
    }

    await signup({
      name: values.name,
      surname: values.surname,
      email: values.email,
      password: values.password,
    })

    ensureDeviceFingerprint()

    const result = await resolveDeviceAfterAuth()
    setDetectedDevice(result.currentDevice)
    setDeviceName(result.currentDevice?.display_name || "")
    setIsDeviceModalOpen(true)
    setAllowAutoRedirect(false)
  })

  const deviceMutation = useUpdateCurrentDeviceMutation({
    onSuccess: () => {
      setIsDeviceModalOpen(false)
      setAllowAutoRedirect(true)
      navigate("/", { replace: true })
    },
    onError: (error) => {
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Failed to save device name"
      setDeviceStepError(String(message))
    },
  })

  if (isAuthenticated && allowAutoRedirect && !isDeviceModalOpen) {
    return <Navigate to="/" replace />
  }

  const isLoading = authMutation.isLoading || deviceMutation.isLoading
  const errorMessage =
    authErrorMessage ||
    authMutation.error?.response?.data?.detail ||
    authMutation.error?.message

  const handleAuthSubmit = (values) => {
    if (mode === "signup") {
      setAllowAutoRedirect(false)
    } else {
      setAllowAutoRedirect(true)
    }
    authMutation.mutate(values)
  }

  const handleDeviceSubmit = (nextDeviceName) => {
    setDeviceStepError("")
    setDeviceName(nextDeviceName)
    deviceMutation.mutate(nextDeviceName)
  }

  const switchMode = (nextMode) => {
    setMode(nextMode)
    setDeviceStepError("")
    setAuthErrorMessage("")
    setDeviceName("")
    setDetectedDevice(null)
    setIsDeviceModalOpen(false)
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

        <DetectedDeviceDialog
          open={isDeviceModalOpen}
          detectedDevice={detectedDevice}
          initialDeviceName={deviceName}
          isLoading={deviceMutation.isLoading}
          errorMessage={deviceStepError}
          onSubmitDeviceName={handleDeviceSubmit}
        />
      </div>
    </div>
  )
}
