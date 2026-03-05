import { useQuery } from "@tanstack/react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { meSidebarRequest } from "@/features/user/api/user-api"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"

export function useUserSidebarQuery() {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: USER_SIDEBAR_QUERY_KEY,
    queryFn: meSidebarRequest,
    enabled: isAuthenticated,
    retry: false,
  })
}
