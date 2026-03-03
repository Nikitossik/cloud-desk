import { useQuery } from "react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { meDevicesRequest } from "@/features/device/api/device-api"
import { USER_DEVICES_QUERY_KEY } from "@/features/device/lib/query-keys"

export function useUserDevicesQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery(USER_DEVICES_QUERY_KEY, meDevicesRequest, {
    enabled: isAuthenticated,
    retry: false,
  })
}
