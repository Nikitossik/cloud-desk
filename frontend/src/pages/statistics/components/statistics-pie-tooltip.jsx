import { SessionAppIcon } from "@/pages/session/components/session-app-icon"
import { Badge } from "@/components/ui/badge"

export function StatisticsPieTooltip({
  active,
  payload,
  formatDuration,
  labelKey,
  appIdKey,
  deletedAtKey,
  showIcon = false,
}) {
  if (!active || !Array.isArray(payload) || payload.length === 0) {
    return null
  }

  const item = payload[0]?.payload
  if (!item) {
    return null
  }

  const label = item?.[labelKey] || "Item"
  const isDeleted = Boolean(deletedAtKey && item?.[deletedAtKey])

  return (
    <div className="bg-background rounded-md border p-2 shadow-sm">
      <div className="flex items-center gap-2">
        {showIcon ? <SessionAppIcon appId={item?.[appIdKey]} appName={label} /> : null}
        <span className="text-sm font-medium">{label}</span>
        {isDeleted ? (
          <Badge variant="destructive" className="h-5 px-1.5 text-[10px]">
            In trash
          </Badge>
        ) : null}
      </div>
      <p className="text-muted-foreground mt-1 text-xs">{formatDuration(item.total_time)}</p>
    </div>
  )
}
