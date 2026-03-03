import { useQuery } from "react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { getCurrentDeviceRequest } from "@/features/device/api/device-api"
import { CURRENT_DEVICE_QUERY_KEY } from "@/features/device/lib/query-keys"

export function useCurrentDeviceQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery(CURRENT_DEVICE_QUERY_KEY, getCurrentDeviceRequest, {
    enabled: isAuthenticated,
    retry: false,
  })
}
