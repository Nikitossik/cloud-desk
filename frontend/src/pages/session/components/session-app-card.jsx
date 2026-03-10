import { AppWindow } from "lucide-react"
import { Badge } from "@/components/ui/badge"

function formatAppDisplayName(name) {
  const baseName = typeof name === "string"
    ? name.replace(/\.exe$/i, "").trim()
    : ""

  if (!baseName) {
    return "Unknown app"
  }

  return baseName.charAt(0).toUpperCase() + baseName.slice(1)
}

export function SessionAppCard({ app }) {
  const isOpened = Boolean(app?.is_active)
  const appName = formatAppDisplayName(app?.name)

  return (
    <div className="bg-background rounded-lg border p-3">
      <div className="flex items-start gap-3">
        <div className="bg-muted rounded-md p-2">
          <AppWindow className="text-muted-foreground size-4" />
        </div>

        <div className="min-w-0 flex-1 space-y-2">
          <p className="truncate text-sm font-medium">{appName}</p>
          <Badge
            variant="outline"
            className={isOpened ? "text-green-600" : "text-muted-foreground"}
          >
            {isOpened ? "Was opened" : "Was closed"}
          </Badge>
        </div>
      </div>
    </div>
  )
}
