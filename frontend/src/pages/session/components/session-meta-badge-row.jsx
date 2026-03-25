import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { formatUiDurationSeconds } from "@/shared/lib/date-time"

export function SessionMetaBadgeRow({
  isDeleted,
  isActive,
  statusText,
  createdAtText,
  hasLastActiveAt,
  lastActiveAtText,
  hasRestoredAt,
  restoredAtText,
  hasDeletedAt,
  deletedAtText,
}) {
  const isCountingActiveTime = Boolean(isActive && !isDeleted)
  const [activeSeconds, setActiveSeconds] = useState(0)

  useEffect(() => {
    if (!isCountingActiveTime) {
      setActiveSeconds(0)
      return () => {}
    }

    setActiveSeconds(0)
    const intervalId = setInterval(() => {
      setActiveSeconds((previous) => previous + 1)
    }, 1000)

    return () => clearInterval(intervalId)
  }, [isCountingActiveTime])

  const activeTimeText = formatUiDurationSeconds(activeSeconds)

  return (
    <Badge variant="outline" className="gap-2 px-3 py-1 text-sm">
      <span
        className={`size-2 rounded-full ${isDeleted ? "bg-red-500" : isActive ? "bg-green-500" : "bg-zinc-500"}`}
      />
      {statusText}
      {isCountingActiveTime ? <span className="font-semibold">{activeTimeText}</span> : null}
      <span className="text-muted-foreground">•</span>
      <span>Created at {createdAtText}</span>
      {!isDeleted && !isActive && hasLastActiveAt ? (
        <>
          <span className="text-muted-foreground">•</span>
          <span>Last active at {lastActiveAtText}</span>
        </>
      ) : null}
      {hasRestoredAt ? (
        <>
          <span className="text-muted-foreground">•</span>
          <span>Restored at {restoredAtText}</span>
        </>
      ) : null}
      {isDeleted && hasDeletedAt ? (
        <>
          <span className="text-muted-foreground">•</span>
          <span>Deleted at {deletedAtText}</span>
        </>
      ) : null}
    </Badge>
  )
}
