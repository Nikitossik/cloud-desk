import { formatUiDateTime } from "@/shared/lib/date-time"

export function TrashSessionCard({ session }) {
  const slug = session?.slugname || session?.slug || ""
  const deletedAtText = formatUiDateTime(session?.deleted_at, {
    withSeconds: false,
    todayAsTime: true,
  })

  if (!slug) {
    return null
  }

  return (
    <a
      href={`/session/trash/${slug}`}
      className="bg-card text-card-foreground rounded-xl border p-4 text-left transition-colors hover:bg-accent/40 cursor-pointer"
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
  )
}
