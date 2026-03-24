import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { getStatisticsAppsRequest, getStatisticsSessionsRequest } from "@/features/statistics/api/statistics-api"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { StatisticsTab } from "@/pages/statistics/components/statistics-tab"
import { formatUiDurationSeconds } from "@/shared/lib/date-time"

export function StatisticsPage() {
  const [activeTab, setActiveTab] = useState("applications")

  const {
    data: appsData,
    isLoading: isAppsLoading,
    error: appsError,
  } = useQuery({
    queryKey: ["statistics", "apps"],
    queryFn: getStatisticsAppsRequest,
    retry: false,
  })

  const {
    data: sessionsData,
    isLoading: isSessionsLoading,
    error: sessionsError,
  } = useQuery({
    queryKey: ["statistics", "sessions"],
    queryFn: getStatisticsSessionsRequest,
    retry: false,
  })

  const applications = Array.isArray(appsData) ? appsData : []
  const sessions = Array.isArray(sessionsData) ? sessionsData : []

  const isLoading = activeTab === "applications" ? isAppsLoading : isSessionsLoading
  const activeError = activeTab === "applications" ? appsError : sessionsError

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <h1 className="text-2xl font-semibold">Statistics</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="applications">Applications</TabsTrigger>
          <TabsTrigger value="sessions">Sessions</TabsTrigger>
        </TabsList>

        <TabsContent value="applications" className="mt-2">
          <StatisticsTab
            tab="applications"
            applications={applications}
            isLoading={isLoading}
            error={activeError}
            formatDuration={formatUiDurationSeconds}
          />
        </TabsContent>

        <TabsContent value="sessions" className="mt-2">
          <StatisticsTab
            tab="sessions"
            sessions={sessions}
            isLoading={isLoading}
            error={activeError}
            formatDuration={formatUiDurationSeconds}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
