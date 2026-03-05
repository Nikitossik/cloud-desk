import { useParams } from "react-router"
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
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useSessionBySlugQuery } from "@/features/session/hooks/use-session-by-slug-query"
import { formatUiDateTime } from "@/shared/lib/date-time"

export function SessionPage() {
  const { session_slug = "" } = useParams()
  const {
    data: session,
    isLoading,
    error,
  } = useSessionBySlugQuery(session_slug)

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
            <DropdownMenuItem>
              <Pencil />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Copy />
              Clone
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem variant="destructive">
              <Trash2 />
              Move to Trash
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

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
    </div>
  );
}
