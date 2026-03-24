import { useEffect, useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import { getDeletedSessionsRequest, purgeSessionTrashRequest } from "@/features/session/api/session-api"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
import { TrashSessionCard } from "@/pages/trash/components/trash-session-card"

export function TrashPage() {
  const queryClient = useQueryClient()
  const [selectedSessionIds, setSelectedSessionIds] = useState([])
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

  useEffect(() => {
    const existingIds = new Set(sessions.map((session) => String(session?.id || "")).filter(Boolean))
    setSelectedSessionIds((previous) => previous.filter((id) => existingIds.has(id)))
  }, [sessions])

  const purgeMutation = useMutation({
    mutationFn: async (payload) => purgeSessionTrashRequest(payload),
    onSuccess: () => {
      setSelectedSessionIds([])
      queryClient.invalidateQueries({ queryKey: ["session", "trash"] })
      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
    },
  })

  const selectedCount = selectedSessionIds.length

  const handleToggleSession = (sessionId, isChecked) => {
    const normalizedId = String(sessionId || "")
    if (!normalizedId) {
      return
    }

    setSelectedSessionIds((previous) => {
      if (isChecked) {
        return previous.includes(normalizedId)
          ? previous
          : [...previous, normalizedId]
      }

      return previous.filter((id) => id !== normalizedId)
    })
  }

  const handlePurge = () => {
    if (selectedCount > 0) {
      purgeMutation.mutate({
        all: false,
        session_ids: selectedSessionIds,
      })
      return
    }

    purgeMutation.mutate({
      all: true,
    })
  }

  const purgeError =
    purgeMutation.error?.response?.data?.detail ||
    purgeMutation.error?.message ||
    ""

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">Trash</h1>
        <Button
          variant="destructive"
          disabled={isLoading || purgeMutation.isPending || sessions.length === 0}
          onClick={handlePurge}
        >
          {purgeMutation.isPending
            ? "Deleting..."
            : selectedCount > 0
              ? `Delete checked (${selectedCount})`
              : "Clear Trash"}
        </Button>
      </div>

      {purgeError ? (
        <p className="text-destructive text-sm">{String(purgeError)}</p>
      ) : null}

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
            const sessionId = String(session?.id || "")
            return (
              <TrashSessionCard
                key={slug || session?.id || session?.name || "deleted-session"}
                session={session}
                checked={selectedSessionIds.includes(sessionId)}
                onCheckedChange={(isChecked) => handleToggleSession(sessionId, isChecked)}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}
