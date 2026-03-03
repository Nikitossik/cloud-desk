import { useQuery } from "@tanstack/react-query"
import { meRequest } from "@/features/user/api/user-api"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { USER_PROFILE_QUERY_KEY } from "@/features/user/lib/query-keys"

export function useUserProfileQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: USER_PROFILE_QUERY_KEY,
    queryFn: meRequest,
    enabled: isAuthenticated,
    retry: false,
  })
}
