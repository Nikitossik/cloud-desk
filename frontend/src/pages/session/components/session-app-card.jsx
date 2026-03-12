import { Badge } from "@/components/ui/badge"
import { SessionAppIcon } from "@/pages/session/components/session-app-icon"

export function SessionAppCard({ app }) {
  const isOpened = Boolean(app?.is_active)
  const appName = app?.display_name
  const appId = app?.app_id
  const isSessionActive = Boolean(app?.is_session_active)
  const statusLabel = isSessionActive
    ? (isOpened ? "Running" : "Closed")
    : (isOpened ? "Was running" : "Was closed")
  const statusVariant = isOpened
    ? (isSessionActive ? "secondary" : "outline")
    : "outline"
  const statusClass = isOpened
    ? isSessionActive
      ? "bg-green-50 text-green-700 border-green-700"
      : "text-green-700 border-green-700"
    : "text-muted-foreground";

  return (
    <div className="bg-background rounded-lg border p-3">
      <div className="flex items-start gap-3">
        <SessionAppIcon appId={appId} appName={appName} />

        <div className="min-w-0 flex-1 space-y-2">
          <p className="truncate text-sm font-medium">{appName}</p>
          <Badge
            variant={statusVariant}
            className={statusClass}
          >
            {statusLabel}
          </Badge>
        </div>
      </div>
    </div>
  )
}
