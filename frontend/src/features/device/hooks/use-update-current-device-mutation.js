import { useMutation, useQueryClient } from "@tanstack/react-query"
import { updateCurrentDeviceRequest } from "@/features/device/api/device-api"
import {
  CURRENT_DEVICE_QUERY_KEY,
  USER_DEVICES_QUERY_KEY,
} from "@/features/device/lib/query-keys"

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

      await options.onSuccess?.(data, variables, context)
    },
  })
}
