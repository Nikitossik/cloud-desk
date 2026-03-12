import { useNavigate, useParams } from "react-router"
import { useRef, useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import {
  Pencil,
  RotateCcw,
  Trash2,
  Ellipsis,
} from "lucide-react"
import { FaPlay, FaPause } from "react-icons/fa"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  deleteActiveSessionRequest,
  deleteSessionByIdRequest,
  restoreActiveSessionRequest,
  restoreSessionByIdRequest,
  startSessionByIdRequest,
  stopActiveSessionRequest,
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
import { useActiveSessionAppsWs } from "@/features/session/hooks/use-active-session-apps-ws"
import { useSessionAppsBySlugQuery } from "@/features/session/hooks/use-session-apps-by-slug-query"
import { useSessionBySlugQuery } from "@/features/session/hooks/use-session-by-slug-query"
import { SessionAppCard } from "@/pages/session/components/session-app-card"
import { SessionDialog } from "@/features/session/components/session-dialog"
import { formatUiDateTime } from "@/shared/lib/date-time"

export function SessionPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { session_slug = "" } = useParams()
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const shouldStopActiveRef = useRef(false)
  const {
    data: session,
    isLoading,
    error,
  } = useSessionBySlugQuery(session_slug)
  const {
    data: sessionApps,
    isLoading: isSessionAppsLoading,
    error: sessionAppsError,
  } = useSessionAppsBySlugQuery(session_slug, Boolean(session && !session.is_active))

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

  const sessionActionMutation = useMutation({
    mutationFn: async ({ action, isActive, sessionId }) => {
      if (action === "start") {
        const data = await startSessionByIdRequest(sessionId)
        shouldStopActiveRef.current = true
        return data
      }

      if (action === "stop") {
        const mustUseActiveStop = Boolean(isActive) || shouldStopActiveRef.current
        const data = mustUseActiveStop
          ? await stopActiveSessionRequest()
          : null

        shouldStopActiveRef.current = false
        return data
      }

      if (action === "restore") {
        return isActive
          ? restoreActiveSessionRequest()
          : restoreSessionByIdRequest(sessionId)
      }

      return null
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      queryClient.invalidateQueries({ queryKey: SESSION_BY_SLUG_QUERY_KEY(session_slug) })
    },
  })

  const actionError =
    sessionActionMutation.error?.response?.data?.detail ||
    sessionActionMutation.error?.message ||
    ""

  const isActive = Boolean(session?.is_active)
  const {
    apps: activeSessionApps,
    isLoading: isActiveAppsLoading,
    error: activeAppsError,
  } = useActiveSessionAppsWs(Boolean(session && isActive))
  const statusText = isActive ? "Active" : "Inactive"
  const createdAtText = formatUiDateTime(session?.created_at, {
    withSeconds: false,
    todayAsTime: true,
  })
  const hasLastActiveAt = Boolean(session?.last_active_at)
  const lastActiveAtText = formatUiDateTime(session?.last_active_at, {
    withSeconds: false,
    todayAsTime: true,
  })
  const visibleApps = isActive ? activeSessionApps : sessionApps

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

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">
          {session.name}
        </h1>

        {session.description ? (
          <p className="text-muted-foreground max-w-3xl leading-relaxed">
            {session.description}
          </p>
        ) : null}
      </div>

      {deleteError ? (
        <p className="text-destructive text-sm">{String(deleteError)}</p>
      ) : null}
      {actionError ? (
        <p className="text-destructive text-sm">{String(actionError)}</p>
      ) : null}

      <div className="flex items-start justify-between gap-4">
        <Badge variant="outline" className="gap-2 px-3 py-1 text-sm">
          <span
            className={`size-2 rounded-full ${isActive ? "bg-green-500" : "bg-zinc-500"}`}
          />
          {statusText}
          <span className="text-muted-foreground">•</span>
          <span>Created at {createdAtText}</span>
          {!isActive && hasLastActiveAt ? (
            <>
              <span className="text-muted-foreground">•</span>
              <span>Last active at {lastActiveAtText}</span>
            </>
          ) : null}
        </Badge>

        <div className="flex items-center gap-2">
          <Button
            className="gap-2 cursor-pointer"
            disabled={sessionActionMutation.isPending}
            onClick={() => {
              if (isActive || shouldStopActiveRef.current) {
                sessionActionMutation.mutate({
                  action: "stop",
                  isActive,
                  sessionId: session.id,
                });
                return;
              }

              sessionActionMutation.mutate({
                action: "start",
                isActive,
                sessionId: session.id,
              });
            }}
          >
            {isActive ? (
              <FaPause className="size-3" />
            ) : (
              <FaPlay className="size-3" />
            )}
            {isActive ? "Stop" : "Start"}
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="gap-2">
                <Ellipsis className="size-4" />
                Actions
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuItem
                disabled={sessionActionMutation.isPending}
                onClick={(event) => {
                  event.preventDefault();
                  sessionActionMutation.mutate({
                    action: "restore",
                    isActive,
                    sessionId: session.id,
                  });
                }}
              >
                <RotateCcw />
                Restore
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={(event) => {
                  event.preventDefault();
                  setIsEditDialogOpen(true);
                }}
              >
                <Pencil />
                Edit
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                variant="destructive"
                disabled={deleteSessionMutation.isPending}
                onClick={(event) => {
                  event.preventDefault();
                  deleteSessionMutation.mutate({
                    isActive: session.is_active,
                    sessionId: session.id,
                  });
                }}
              >
                <Trash2 />
                {deleteSessionMutation.isPending
                  ? "Deleting..."
                  : "Move to Trash"}
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      <section className="bg-card text-card-foreground rounded-xl border p-4">
        <h2 className="text-xl font-semibold">Applications</h2>

        {isActive ? (
          isActiveAppsLoading ? (
            <p className="text-muted-foreground mt-2 text-sm">
              Loading live applications...
            </p>
          ) : activeAppsError ? (
            <p className="text-destructive mt-2 text-sm">{activeAppsError}</p>
          ) : Array.isArray(visibleApps) && visibleApps.length > 0 ? (
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {visibleApps.map((app) => {
                const appKey =
                  app?.state_id || app?.app_id || app?.name || "unknown-app";
                return (
                  <SessionAppCard
                    key={appKey}
                    app={{ ...app, is_session_active: true }}
                  />
                );
              })}
            </div>
          ) : (
            <p className="text-muted-foreground mt-2 text-sm">
              No applications in active session.
            </p>
          )
        ) : isSessionAppsLoading ? (
          <p className="text-muted-foreground mt-2 text-sm">
            Loading applications...
          </p>
        ) : sessionAppsError ? (
          <p className="text-destructive mt-2 text-sm">
            {String(
              sessionAppsError?.response?.data?.detail ||
                sessionAppsError?.message ||
                "Failed to load applications",
            )}
          </p>
        ) : Array.isArray(visibleApps) && visibleApps.length > 0 ? (
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {visibleApps.map((app) => {
              const appKey =
                app?.state_id || app?.app_id || app?.name || "unknown-app";
              return (
                <SessionAppCard
                  key={appKey}
                  app={{ ...app, is_session_active: false }}
                />
              );
            })}
          </div>
        ) : (
          <p className="text-muted-foreground mt-2 text-sm">
            No applications in this session.
          </p>
        )}
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
