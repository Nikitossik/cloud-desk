import { useQuery } from "@tanstack/react-query"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { getSessionBySlugRequest } from "@/features/session/api/session-api"
import { SESSION_BY_SLUG_QUERY_KEY } from "@/features/session/lib/query-keys"

export function useSessionBySlugQuery(sessionSlug) {
  const { isAuthenticated } = useAuth()

  return useQuery({
    queryKey: SESSION_BY_SLUG_QUERY_KEY(sessionSlug),
    queryFn: () => getSessionBySlugRequest(sessionSlug),
    enabled: isAuthenticated && Boolean(sessionSlug),
    retry: false,
  })
}
