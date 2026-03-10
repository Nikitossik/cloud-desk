import { useQuery } from "@tanstack/react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { getSessionAppsBySlugRequest } from "@/features/session/api/session-api"
import { SESSION_APPS_BY_SLUG_QUERY_KEY } from "@/features/session/lib/query-keys"

export function useSessionAppsBySlugQuery(sessionSlug, enabled = true) {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: SESSION_APPS_BY_SLUG_QUERY_KEY(sessionSlug),
    queryFn: () => getSessionAppsBySlugRequest(sessionSlug),
    enabled: isAuthenticated && Boolean(sessionSlug) && enabled,
    retry: false,
  })
}
