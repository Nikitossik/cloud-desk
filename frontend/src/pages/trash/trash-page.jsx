import { useQuery } from "@tanstack/react-query"
import { useNavigate } from "react-router"
import { getDeletedSessionsRequest } from "@/features/session/api/session-api"

export function TrashPage() {
  const navigate = useNavigate()
  const {
    data,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["session", "deleted"],
    queryFn: getDeletedSessionsRequest,
    retry: false,
  })
  const sessions = Array.isArray(data) ? data : []

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <h1 className="text-2xl font-semibold">Trash</h1>

      {isLoading ? (
        <p className="text-muted-foreground">Loading deleted sessions...</p>
      ) : error ? (
        <p className="text-destructive text-sm">
          {String(error?.response?.data?.detail || error?.message || "Failed to load deleted sessions")}
        </p>
      ) : sessions.length === 0 ? (
        <p className="text-muted-foreground">Trash is empty.</p>
      ) : (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {sessions.map((session) => {
            const slug = session?.slugname || session?.slug || ""
            if (!slug) {
              return null
            }

            return (
              <button
                key={slug}
                type="button"
                className="bg-card text-card-foreground rounded-xl border p-4 text-left transition-colors hover:bg-accent/40"
                onClick={() => navigate(`/session/trash/${slug}`)}
              >
                <p className="truncate font-medium">{session?.name || "Unnamed session"}</p>
                {session?.description ? (
                  <p className="text-muted-foreground mt-1 line-clamp-2 text-sm">
                    {session.description}
                  </p>
                ) : null}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
