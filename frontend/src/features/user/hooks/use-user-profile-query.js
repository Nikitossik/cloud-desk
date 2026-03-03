import { useQuery } from "react-query"
import { meRequest } from "@/features/user/api/user-api"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { USER_PROFILE_QUERY_KEY } from "@/features/user/lib/query-keys"

export function useUserProfileQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery(USER_PROFILE_QUERY_KEY, meRequest, {
    enabled: isAuthenticated,
    retry: false,
  })
}
