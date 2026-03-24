import { StatisticsSessionCard } from "@/pages/statistics/components/statistics-session-card"
import { StatisticsSessionAppCard } from "@/pages/statistics/components/statistics-session-app-card"

export function StatisticsTab({
  tab,
  sessions,
  applications,
  isLoading,
  error,
  formatDuration,
  allSessions = true,
  onAllSessionsChange,
}) {
  if (isLoading) {
    return <p className="text-muted-foreground">Loading statistics...</p>
  }

  if (error) {
    return (
      <p className="text-destructive text-sm">
        {String(error?.response?.data?.detail || error?.message || "Failed to load statistics")}
      </p>
    )
  }

  if (tab === "applications") {
    if (!Array.isArray(applications) || applications.length === 0) {
      return <p className="text-muted-foreground">No application usage statistics yet.</p>
    }

    return (
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {applications.map((application) => {
          const usageItems = Array.isArray(application?.usage) ? application.usage : []
          const totalTime = Number(application?.total_time || 0)

          return (
            <StatisticsSessionAppCard
              key={String(application?.app_id || application?.display_name || "app")}
              app={{
                app_id: application?.app_id,
                display_name: application?.display_name,
                total_time: totalTime,
              }}
              formatDuration={formatDuration}
              usage={usageItems}
            />
          )
        })}
      </div>
    )
  }

  if (!Array.isArray(sessions) || sessions.length === 0) {
    return (
      <div className="space-y-3">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={allSessions}
            onChange={(event) => onAllSessionsChange?.(event.target.checked)}
          />
          <span className="text-muted-foreground">Show sessions from trash</span>
        </label>
        <p className="text-muted-foreground">No session usage statistics yet.</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={allSessions}
          onChange={(event) => onAllSessionsChange?.(event.target.checked)}
        />
        <span className="text-muted-foreground">Show sessions from trash</span>
      </label>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {sessions.map((session) => (
          <StatisticsSessionCard
            key={String(session?.session_id || session?.session_name || "session")}
            session={session}
            formatDuration={formatDuration}
          />
        ))}
      </div>
    </div>
  )
}
