import { useQuery } from "@tanstack/react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { meDevicesRequest } from "@/features/device/api/device-api"
import { USER_DEVICES_QUERY_KEY } from "@/features/device/lib/query-keys"

export function useUserDevicesQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: USER_DEVICES_QUERY_KEY,
    queryFn: meDevicesRequest,
    enabled: isAuthenticated,
    retry: false,
  })
}
