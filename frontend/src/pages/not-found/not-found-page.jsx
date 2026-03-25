import { Link } from "react-router"
import { SearchX } from "lucide-react"
import { Button } from "@/components/ui/button"

export function NotFoundPage({
  title = "Page not found",
  message = "We couldn't find the page you requested.",
  primaryActionTo = "/statistics",
  primaryActionLabel = "Go to statistics",
}) {
  return (
    <div className="flex flex-1 items-center justify-center p-4 pt-0">
      <div className="bg-card text-card-foreground w-full max-w-xl rounded-2xl border p-8 shadow-sm">
        <div className="bg-muted mb-4 inline-flex size-12 items-center justify-center rounded-xl">
          <SearchX className="size-6" />
        </div>

        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        <p className="text-muted-foreground mt-3 leading-relaxed">{message}</p>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <Button asChild>
            <Link to={primaryActionTo}>{primaryActionLabel}</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/">Back to home</Link>
          </Button>
        </div>
      </div>
    </div>
  )
}