import { useQuery } from "@tanstack/react-query"
import { getDeletedSessionsRequest } from "@/features/session/api/session-api"
import { TrashSessionCard } from "@/pages/trash/components/trash-session-card"

export function TrashPage() {
  const {
    data,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["session", "trash"],
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
            return (
              <TrashSessionCard
                key={slug || session?.id || session?.name || "deleted-session"}
                session={session}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}
