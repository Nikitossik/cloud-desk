import { MonitorX } from "lucide-react"
import { Badge } from "@/components/ui/badge"

function normalizeDeviceOs(deviceOs) {
  const normalized = (deviceOs || "").trim()
  return normalized || "Unknown"
}

export function UnsupportedDevicePage({ deviceOs, reason }) {
  const normalizedDeviceOs = normalizeDeviceOs(deviceOs)

  return (
    <div className="flex flex-1 items-center justify-center p-4 pt-0">
      <div className="bg-card text-card-foreground w-full max-w-2xl rounded-2xl border p-8 shadow-sm">
        <div className="bg-muted mb-4 inline-flex size-12 items-center justify-center rounded-xl">
          <MonitorX className="size-6" />
        </div>

        <div className="mb-3 flex flex-wrap items-center gap-2">
          <Badge variant="secondary">Unsupported device</Badge>
          <Badge variant="outline">Detected OS: {normalizedDeviceOs}</Badge>
        </div>

        <h1 className="text-3xl font-semibold tracking-tight">Core features are not available on this device</h1>

        <p className="text-muted-foreground mt-3 leading-relaxed">
          CloudDesk currently works with desktop Windows devices only. Support for macOS,
          Linux, Android, and iOS is coming soon.
        </p>

        {reason ? (
          <div className="bg-muted/60 mt-5 rounded-xl border p-4">
            <p className="text-sm leading-relaxed">{reason}</p>
          </div>
        ) : null}
      </div>
    </div>
  )
}
