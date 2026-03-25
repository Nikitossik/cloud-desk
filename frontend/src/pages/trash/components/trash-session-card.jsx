import { formatUiDateTime } from "@/shared/lib/date-time"

export function TrashSessionCard({ session, checked = false, onCheckedChange }) {
  const slug = session?.slugname || session?.slug || ""
  const deletedAtText = formatUiDateTime(session?.last_deleted_at, {
    withSeconds: false,
    todayAsTime: true,
  })

  if (!slug) {
    return null
  }

  return (
    <div className="bg-card text-card-foreground rounded-xl border p-4 transition-colors hover:bg-accent/40">
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          className="h-4 w-4 cursor-pointer"
          checked={checked}
          onChange={(event) => onCheckedChange?.(event.target.checked)}
          aria-label={`Select ${session?.name || "session"}`}
        />

        <a
          href={`/session/trash/${slug}`}
          className="block min-w-0 flex-1 text-left cursor-pointer"
        >
          <p className="truncate font-medium">{session?.name || "Unnamed session"}</p>
          {session?.description ? (
            <p className="text-muted-foreground mt-1 line-clamp-2 text-sm">
              {session.description}
            </p>
          ) : null}
          <p className="text-muted-foreground mt-2 text-xs">
            Deleted at {deletedAtText}
          </p>
        </a>
      </div>
    </div>
  )
}
