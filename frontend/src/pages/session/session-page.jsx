import { useParams } from "react-router"
import {
  Copy,
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

const mockSessionBySlug = {
  "my-first-session": {
    name: "My First Session",
    description:
      "This is a mock description for the selected session. Here you will see full session details, apps state, and usage history.",
    status: "Inactive",
  },
}

export function SessionPage() {
  const { session_slug } = useParams()
  const session = mockSessionBySlug[session_slug] ?? {
    name: `Session ${session_slug}`,
    description:
      "This is a mock description for the selected session. Here you will see full session details, apps state, and usage history.",
    status: "Inactive",
  }

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="flex items-start justify-between gap-4">
        <h1 className="text-3xl font-semibold tracking-tight">{session.name}</h1>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="gap-2">
              <Ellipsis className="size-4" />
              Actions
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuItem>
              <Pencil />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Copy />
              Clone
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Play />
              Activate
            </DropdownMenuItem>
            <DropdownMenuItem>
              <RotateCcw />
              Restore
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
          <span className="size-2 rounded-full bg-zinc-500" />
          {session.status}
        </Badge>
      </div>

      <p className="text-muted-foreground max-w-3xl leading-relaxed">
        {session.description}
      </p>

      <section className="bg-card text-card-foreground rounded-xl border p-4">
        <h2 className="text-xl font-semibold">Applications</h2>
      </section>
    </div>
  )
}
