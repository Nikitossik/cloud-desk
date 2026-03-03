import { useCallback } from "react"
import { useQueryClient } from "@tanstack/react-query"
import {
  getCurrentDeviceRequest,
  meDevicesRequest,
} from "@/features/device/api/device-api"
import {
  CURRENT_DEVICE_QUERY_KEY,
  USER_DEVICES_QUERY_KEY,
} from "@/features/device/lib/query-keys"
import {
  getDeviceFingerprint,
  setDeviceFingerprint,
} from "@/features/device/lib/fingerprint"

export function useResolveDeviceAfterAuth() {
  const queryClient = useQueryClient()

  return useCallback(async () => {
    let fingerprint = getDeviceFingerprint()

    let knownDevices = []
    try {
      knownDevices = await queryClient.fetchQuery({
        queryKey: USER_DEVICES_QUERY_KEY,
        queryFn: meDevicesRequest,
      })
    } catch {
      knownDevices = []
    }

    if (!fingerprint && knownDevices.length === 1) {
      setDeviceFingerprint(knownDevices[0].fingerprint)
      fingerprint = knownDevices[0].fingerprint
    }

    let wasKnown = Boolean(
      fingerprint && knownDevices.some((device) => device.fingerprint === fingerprint)
    )

    let current = null
    try {
      current = await queryClient.fetchQuery({
        queryKey: CURRENT_DEVICE_QUERY_KEY,
        queryFn: getCurrentDeviceRequest,
      })
    } catch {
      current = null
    }

    let refreshedDevices = []
    try {
      refreshedDevices = await queryClient.fetchQuery({
        queryKey: USER_DEVICES_QUERY_KEY,
        queryFn: meDevicesRequest,
      })
    } catch {
      refreshedDevices = []
    }

    if (!wasKnown && fingerprint) {
      wasKnown = refreshedDevices.some((device) => device.fingerprint === fingerprint)
    }

    if (!current && fingerprint) {
      current =
        refreshedDevices.find((device) => device.fingerprint === fingerprint) || null

      if (current) {
        queryClient.setQueryData(CURRENT_DEVICE_QUERY_KEY, current)
      }
    }

    return {
      wasKnown,
      currentDevice: current,
    }
  }, [queryClient])
}
