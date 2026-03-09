import { useNavigate, useParams } from "react-router"
import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import {
  Copy,
  Pause,
  Pencil,
  Play,
  RotateCcw,
  Trash2,
  Ellipsis,
} from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  deleteActiveSessionRequest,
  deleteSessionByIdRequest,
} from "@/features/session/api/session-api"
import { SESSION_BY_SLUG_QUERY_KEY } from "@/features/session/lib/query-keys"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useSessionBySlugQuery } from "@/features/session/hooks/use-session-by-slug-query"
import { SessionDialog } from "@/features/session/components/session-dialog"
import { formatUiDateTime } from "@/shared/lib/date-time"

export function SessionPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { session_slug = "" } = useParams()
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const {
    data: session,
    isLoading,
    error,
  } = useSessionBySlugQuery(session_slug)

  const deleteSessionMutation = useMutation({
    mutationFn: async ({ isActive, sessionId }) => {
      if (isActive) {
        await deleteActiveSessionRequest()
        return
      }

      await deleteSessionByIdRequest(sessionId)
    },
    onSuccess: () => {
      navigate("/statistics", { replace: true })
      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      queryClient.removeQueries({ queryKey: SESSION_BY_SLUG_QUERY_KEY(session_slug) })
    },
  })

  const deleteError =
    deleteSessionMutation.error?.response?.data?.detail ||
    deleteSessionMutation.error?.message ||
    ""

  if (isLoading) {
    return (
      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <p className="text-muted-foreground">Loading session...</p>
      </div>
    )
  }

  if (!session) {
    const errorMessage = error?.response?.data?.detail || error?.message || "Session not found"

    return (
      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <p className="text-destructive">{String(errorMessage)}</p>
      </div>
    )
  }

  const isActive = Boolean(session.is_active)
  const statusText = isActive ? "Active" : "Inactive"
  const createdAtText = formatUiDateTime(session.created_at)

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="flex items-start justify-between gap-4">
        <h1 className="text-3xl font-semibold tracking-tight">
          {session.name}
        </h1>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="gap-2">
              <Ellipsis className="size-4" />
              Actions
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuItem>
              {isActive ? <Pause /> : <Play />}
              {isActive ? "Stop" : "Start"}
            </DropdownMenuItem>
            <DropdownMenuItem>
              <RotateCcw />
              Restore
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={(event) => {
                event.preventDefault()
                setIsEditDialogOpen(true)
              }}
            >
              <Pencil />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Copy />
              Clone
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              variant="destructive"
              disabled={deleteSessionMutation.isPending}
              onClick={(event) => {
                event.preventDefault()
                deleteSessionMutation.mutate({
                  isActive: session.is_active,
                  sessionId: session.id,
                })
              }}
            >
              <Trash2 />
              {deleteSessionMutation.isPending ? "Deleting..." : "Move to Trash"}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {deleteError ? <p className="text-destructive text-sm">{String(deleteError)}</p> : null}

      <div>
        <Badge variant="outline" className="gap-2 px-3 py-1 text-sm">
          <span className={`size-2 rounded-full ${isActive ? "bg-green-500" : "bg-zinc-500"}`} />
          {statusText}
          <span className="text-muted-foreground">•</span>
          <span>Created at {createdAtText}</span>
        </Badge>
      </div>

      {session.description ? (
        <p className="text-muted-foreground max-w-3xl leading-relaxed">
          {session.description}
        </p>
      ) : null}

      <section className="bg-card text-card-foreground rounded-xl border p-4">
        <h2 className="text-xl font-semibold">Applications</h2>
      </section>

      <SessionDialog
        key={`edit-${session.id}-${session.slugname || session_slug}-${isEditDialogOpen}`}
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        mode="edit"
        session={session}
        sessionSlug={session_slug}
      />
    </div>
  );
}
