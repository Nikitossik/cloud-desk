import { useMutation, useQueryClient } from "@tanstack/react-query"
import { updateCurrentDeviceRequest } from "@/features/device/api/device-api"
import {
  CURRENT_DEVICE_QUERY_KEY,
  USER_DEVICES_QUERY_KEY,
} from "@/features/device/lib/query-keys"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"

export function useUpdateCurrentDeviceMutation(options = {}) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (displayName) => updateCurrentDeviceRequest(displayName),
    ...options,
    onSuccess: async (data, variables, context) => {
      queryClient.setQueryData(CURRENT_DEVICE_QUERY_KEY, data)
      queryClient.setQueryData(USER_DEVICES_QUERY_KEY, (prev) => {
        const list = Array.isArray(prev) ? prev : []
        const hasDevice = list.some((device) => device.id === data.id)

        if (!hasDevice) {
          return [...list, data]
        }

        return list.map((device) => (device.id === data.id ? data : device))
      })

      queryClient.setQueryData(USER_SIDEBAR_QUERY_KEY, (prev) => {
        if (!prev || typeof prev !== "object") return prev

        const devices = Array.isArray(prev.devices) ? prev.devices : []
        const hasDevice = devices.some((device) => device.id === data.id)

        const nextDevices = hasDevice
          ? devices.map((device) => (device.id === data.id ? { ...device, ...data } : device))
          : [...devices, data]

        return {
          ...prev,
          devices: nextDevices,
        }
      })

      await options.onSuccess?.(data, variables, context)
    },
  })
}
