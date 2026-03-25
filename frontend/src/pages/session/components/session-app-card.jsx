import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { SessionAppIcon } from "@/pages/session/components/session-app-icon"
import { formatUiDurationSeconds } from "@/shared/lib/date-time"

export function SessionAppCard({ app }) {
  const isOpened = Boolean(app?.is_active)
  const appName = app?.display_name
  const appId = app?.app_id
  const isSessionActive = Boolean(app?.is_session_active)
  const isSessionDeleted = Boolean(app?.is_session_deleted)
  const restoreStatus = app?.restore_status
  const restoreReason = app?.restore_reason
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const effectiveRestoreStatus = isSessionActive ? restoreStatus : null

  const statusLabel = effectiveRestoreStatus
    ? (effectiveRestoreStatus === "launching"
      ? "Launching"
      : (effectiveRestoreStatus === "running" ? "Running" : "Closed"))
    : (isSessionActive
      ? (isOpened ? "Running" : "Closed")
      : (isOpened ? "Was active" : "Was closed"))

  const statusVariant = effectiveRestoreStatus === "launching"
    ? "secondary"
    : (effectiveRestoreStatus === "running"
      ? "secondary"
      : "outline")

  const statusClass = isSessionDeleted
    ? "text-muted-foreground"
    : effectiveRestoreStatus === "launching"
    ? "text-blue-700 border-blue-700"
    : (effectiveRestoreStatus === "running"
      ? "bg-green-50 text-green-700 border-green-700"
      : (effectiveRestoreStatus === "closed"
        ? "text-muted-foreground"
        : (isOpened
          ? (isSessionActive
            ? "bg-green-50 text-green-700 border-green-700"
            : "text-green-700 border-green-700")
          : "text-muted-foreground")))

  const isRunningNow = effectiveRestoreStatus === "running" || (!effectiveRestoreStatus && isSessionActive && isOpened)

  useEffect(() => {
    setElapsedSeconds(0)
  }, [appId])

  useEffect(() => {
    if (!isSessionActive || !isRunningNow) {
      setElapsedSeconds(0)
      return () => {}
    }

    const intervalId = setInterval(() => {
      setElapsedSeconds((previous) => previous + 1)
    }, 1000)

    return () => clearInterval(intervalId)
  }, [isSessionActive, isRunningNow])

  const displayedDuration = formatUiDurationSeconds(elapsedSeconds)

  return (
    <div className="bg-background rounded-lg border p-3">
      <div className="flex items-start gap-3">
        <SessionAppIcon
          appId={appId}
          appName={appName}
          isSessionDeleted={isSessionDeleted}
        />

        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex items-center justify-between gap-2">
            <p className="truncate text-sm font-medium">{appName}</p>
            {isSessionActive && isRunningNow ? (
              <p className="text-sm whitespace-nowrap">{displayedDuration}</p>
            ) : null}
          </div>
          <Badge
            variant={statusVariant}
            className={statusClass}
          >
            {statusLabel}
          </Badge>
          {effectiveRestoreStatus === "closed" && restoreReason ? (
            <p className="text-destructive text-xs leading-tight">
              {restoreReason}
            </p>
          ) : null}
        </div>
      </div>
    </div>
  )
}
