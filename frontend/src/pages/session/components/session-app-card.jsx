import { Badge } from "@/components/ui/badge"
import { SessionAppIcon } from "@/pages/session/components/session-app-icon"

export function SessionAppCard({ app }) {
  const isOpened = Boolean(app?.is_active)
  const appName = app?.display_name
  const appId = app?.app_id
  const isSessionActive = Boolean(app?.is_session_active)
  const isSessionDeleted = Boolean(app?.is_session_deleted)
  const restoreStatus = app?.restore_status
  const restoreReason = app?.restore_reason

  const statusLabel = restoreStatus
    ? (restoreStatus === "launching"
      ? "Launching"
      : (restoreStatus === "running" ? "Running" : "Closed"))
    : (isSessionActive
      ? (isOpened ? "Running" : "Closed")
      : (isOpened ? "Was running" : "Was closed"))

  const statusVariant = restoreStatus === "launching"
    ? "secondary"
    : (restoreStatus === "running"
      ? "secondary"
      : "outline")

  const statusClass = isSessionDeleted
    ? "text-muted-foreground"
    : restoreStatus === "launching"
    ? "text-blue-700 border-blue-700"
    : (restoreStatus === "running"
      ? "bg-green-50 text-green-700 border-green-700"
      : (restoreStatus === "closed"
        ? "text-muted-foreground"
        : (isOpened
          ? (isSessionActive
            ? "bg-green-50 text-green-700 border-green-700"
            : "text-green-700 border-green-700")
          : "text-muted-foreground")))

  return (
    <div className="bg-background rounded-lg border p-3">
      <div className="flex items-start gap-3">
        <SessionAppIcon
          appId={appId}
          appName={appName}
          isSessionDeleted={isSessionDeleted}
        />

        <div className="min-w-0 flex-1 space-y-2">
          <p className="truncate text-sm font-medium">{appName}</p>
          <Badge
            variant={statusVariant}
            className={statusClass}
          >
            {statusLabel}
          </Badge>
          {restoreStatus === "closed" && restoreReason ? (
            <p className="text-destructive text-xs leading-tight">
              {restoreReason}
            </p>
          ) : null}
        </div>
      </div>
    </div>
  )
}
