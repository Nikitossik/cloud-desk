import { useEffect, useState } from "react"
import { getAccessToken } from "@/features/auth/lib/token-storage"
import { getOrCreateDeviceFingerprint } from "@/features/device/lib/fingerprint"
import { connectActiveSessionAppsWebSocket } from "@/features/session/api/session-ws"

export function useActiveSessionAppsWs(enabled) {
  const [apps, setApps] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!enabled) {
      setApps([])
      setIsLoading(false)
      setError("")
      return () => {}
    }

    const token = getAccessToken()
    const fingerprint = getOrCreateDeviceFingerprint()

    setIsLoading(true)
    setError("")

    const socket = connectActiveSessionAppsWebSocket({
      token,
      deviceFingerprint: fingerprint,
    })

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)
        const incomingApps = Array.isArray(payload?.apps) ? payload.apps : []

        if (payload?.type === "snapshot") {
          setApps(incomingApps)
          setIsLoading(false)
          return
        }

        if (payload?.type === "upsert") {
          setApps((previous) => {
            const appsMap = new Map(
              (Array.isArray(previous) ? previous : []).map((item) => [item.app_id, item]),
            )

            incomingApps.forEach((app) => {
              if (app?.app_id) {
                appsMap.set(app.app_id, app)
              }
            })

            return Array.from(appsMap.values())
          })
        }
      } catch {
        setError("Failed to parse live updates")
      }
    }

    socket.onerror = () => {
      setError("Live updates are unavailable")
      setIsLoading(false)
    }

    socket.onclose = () => {
      setIsLoading(false)
    }

    return () => {
      socket.close()
    }
  }, [enabled])

  return {
    apps,
    isLoading,
    error,
  }
}
