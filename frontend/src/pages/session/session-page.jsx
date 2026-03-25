import { useLocation, useNavigate, useParams } from "react-router"
import { useRef, useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import {
  deleteSessionByIdRequest,
  restoreSessionByIdRequest,
  startSessionByIdRequest,
  stopActiveSessionRequest,
  updateSessionByIdRequest,
} from "@/features/session/api/session-api"
import { SESSION_BY_SLUG_QUERY_KEY } from "@/features/session/lib/query-keys"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
import { useActiveSessionAppsWs } from "@/features/session/hooks/use-active-session-apps-ws"
import { useSessionAppsBySlugQuery } from "@/features/session/hooks/use-session-apps-by-slug-query"
import { useSessionBySlugQuery } from "@/features/session/hooks/use-session-by-slug-query"
import { SessionAppCard } from "@/pages/session/components/session-app-card"
import { SessionMetaBadgeRow } from "@/pages/session/components/session-meta-badge-row"
import { SessionActions } from "@/pages/session/components/session-actions"
import { SessionDialog } from "@/features/session/components/session-dialog"
import { formatUiDateTime } from "@/shared/lib/date-time"

export function SessionPage() {
  const navigate = useNavigate()
  const { pathname } = useLocation()
  const queryClient = useQueryClient()
  const { session_slug = "" } = useParams()
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [restoreStatusByAppId, setRestoreStatusByAppId] = useState({})
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

  const isTrashRoute = pathname.startsWith("/session/trash/")

  const updateDeletedMutation = useMutation({
    mutationFn: async ({ sessionId, isDeleted }) => {
      return updateSessionByIdRequest(sessionId, { is_deleted: isDeleted })
    },
    onSuccess: (_, variables) => {
      if (variables?.isDeleted) {
        const sidebarData = queryClient.getQueryData(USER_SIDEBAR_QUERY_KEY)
        const userSessions = Array.isArray(sidebarData?.sessions)
          ? sidebarData.sessions
          : []

        const nextSession = userSessions.find((item) => {
          const itemSlug = item?.slugname || item?.slug || ""
          const itemId = item?.id

          if (!itemSlug) {
            return false
          }

          if (variables?.sessionId && itemId && itemId === variables.sessionId) {
            return false
          }

          return itemSlug !== session_slug
        })

        if (nextSession?.slugname || nextSession?.slug) {
          const nextSlug = nextSession.slugname || nextSession.slug
          navigate(`/session/${nextSlug}`, { replace: true })
        } else {
          navigate("/trash", { replace: true })
        }
      } else {
        navigate(`/session/${session_slug}`, { replace: true })
      }

      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      queryClient.invalidateQueries({ queryKey: ["session", "trash"] })
      queryClient.removeQueries({ queryKey: SESSION_BY_SLUG_QUERY_KEY(session_slug) })
    },
  })

  const deletedStateError =
    updateDeletedMutation.error?.response?.data?.detail ||
    updateDeletedMutation.error?.message ||
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

  const restoreSessionMutation = useMutation({
    mutationFn: async ({ sessionId }) => {
      return restoreSessionByIdRequest(sessionId)
    },
    onMutate: () => {
      const launchingMap = {}
      for (const app of sessionApps || []) {
        if (app?.is_active && app?.app_id) {
          launchingMap[String(app.app_id)] = {
            status: "launching",
            reason: null,
          }
        }
      }
      setRestoreStatusByAppId(launchingMap)
    },
    onSuccess: (response) => {
      const nextStatuses = {}
      const report = Array.isArray(response?.report) ? response.report : []

      for (const item of report) {
        if (!item?.app_id) {
          continue
        }

        const isRunning = item.status === "started" || item.status === "already_running"
        nextStatuses[String(item.app_id)] = {
          status: isRunning ? "running" : "closed",
          reason: item.reason || null,
        }
      }

      setRestoreStatusByAppId(nextStatuses)
      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      queryClient.invalidateQueries({ queryKey: SESSION_BY_SLUG_QUERY_KEY(session_slug) })
    },
  })

  const restoreError =
    restoreSessionMutation.error?.response?.data?.detail ||
    restoreSessionMutation.error?.message ||
    ""

  const deletePermanentMutation = useMutation({
    mutationFn: async ({ sessionId }) => {
      await deleteSessionByIdRequest(sessionId)
    },
    onSuccess: () => {
      navigate("/trash", { replace: true })
      queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      queryClient.invalidateQueries({ queryKey: ["session", "trash"] })
      queryClient.removeQueries({ queryKey: SESSION_BY_SLUG_QUERY_KEY(session_slug) })
    },
  })

  const deletePermanentError =
    deletePermanentMutation.error?.response?.data?.detail ||
    deletePermanentMutation.error?.message ||
    ""

  const isActive = Boolean(session?.is_active)
  const isDeleted = Boolean(isTrashRoute || session?.last_deleted_at || session?.is_deleted)
  const {
    apps: activeSessionApps,
    isLoading: isActiveAppsLoading,
    error: activeAppsError,
  } = useActiveSessionAppsWs(Boolean(session && isActive))
  const statusText = isDeleted ? "Deleted" : isActive ? "Active" : "Inactive"
  const createdAtText = formatUiDateTime(session?.created_at, {
    withSeconds: false,
    todayAsTime: true,
  })
  const hasLastActiveAt = Boolean(session?.last_active_at)
  const lastActiveAtText = formatUiDateTime(session?.last_active_at, {
    withSeconds: false,
    todayAsTime: true,
  })
  const hasRestoredAt = Boolean(session?.last_restored_at)
  const restoredAtText = formatUiDateTime(session?.last_restored_at, {
    withSeconds: false,
    todayAsTime: true,
  })
  const hasDeletedAt = Boolean(session?.last_deleted_at)
  const deletedAtText = formatUiDateTime(session?.last_deleted_at, {
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

  const handleRestoreFromTrash = () => {
    updateDeletedMutation.mutate({
      sessionId: session.id,
      isDeleted: false,
    })
  }

  const handleToggleStartStop = () => {
    if (isActive || shouldStopActiveRef.current) {
      sessionActionMutation.mutate({
        action: "stop",
        isActive,
        sessionId: session.id,
      })
      return
    }

    sessionActionMutation.mutate({
      action: "start",
      isActive,
      sessionId: session.id,
    })
  }

  const handleRestore = () => {
    restoreSessionMutation.mutate({
      sessionId: session.id,
    })
  }

  const handleMoveToTrash = () => {
    updateDeletedMutation.mutate({
      sessionId: session.id,
      isDeleted: true,
    })
  }

  const handleDeletePermanently = () => {
    deletePermanentMutation.mutate({
      sessionId: session.id,
    })
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

      {deletedStateError ? (
        <p className="text-destructive text-sm">{String(deletedStateError)}</p>
      ) : null}
      {actionError ? (
        <p className="text-destructive text-sm">{String(actionError)}</p>
      ) : null}
      {restoreError ? (
        <p className="text-destructive text-sm">{String(restoreError)}</p>
      ) : null}
      {deletePermanentError ? (
        <p className="text-destructive text-sm">{String(deletePermanentError)}</p>
      ) : null}

      <div className="flex items-start justify-between gap-4">
        <SessionMetaBadgeRow
          isDeleted={isDeleted}
          isActive={isActive}
          statusText={statusText}
          createdAtText={createdAtText}
          hasLastActiveAt={hasLastActiveAt}
          lastActiveAtText={lastActiveAtText}
          hasRestoredAt={hasRestoredAt}
          restoredAtText={restoredAtText}
          hasDeletedAt={hasDeletedAt}
          deletedAtText={deletedAtText}
        />

        <SessionActions
          isDeleted={isDeleted}
          isActive={isActive}
          isUpdateDeletedPending={updateDeletedMutation.isPending}
          isDeletePermanentPending={deletePermanentMutation.isPending}
          isSessionActionPending={sessionActionMutation.isPending}
          isRestorePending={restoreSessionMutation.isPending}
          onRestoreFromTrash={handleRestoreFromTrash}
          onDeletePermanently={handleDeletePermanently}
          onToggleStartStop={handleToggleStartStop}
          onRestore={handleRestore}
          onEdit={() => setIsEditDialogOpen(true)}
          onMoveToTrash={handleMoveToTrash}
        />
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
                    app={{ ...app, is_session_active: true, is_session_deleted: false }}
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
              const restoreState = app?.app_id
                ? restoreStatusByAppId[String(app.app_id)]
                : null
              return (
                <SessionAppCard
                  key={appKey}
                  app={{
                    ...app,
                    is_session_active: false,
                    is_session_deleted: isDeleted,
                    restore_status: restoreState?.status,
                    restore_reason: restoreState?.reason,
                  }}
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
        key={`edit-${session.id}-${session.slugname || session_slug}-${isTrashRoute}-${isEditDialogOpen}`}
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        mode="edit"
        session={session}
        sessionSlug={session_slug}
      />
    </div>
  );
}
