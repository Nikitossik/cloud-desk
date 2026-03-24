import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"
import { StatisticsPieTooltip } from "@/pages/statistics/components/statistics-pie-tooltip"

const CHART_COLORS = [
  "var(--chart-1)",
  "var(--chart-2)",
  "var(--chart-3)",
  "var(--chart-4)",
  "var(--chart-5)",
]

export function StatisticsSessionCard({ session, formatDuration }) {
  const usageItems = Array.isArray(session?.usage) ? session.usage : []
  const chartData = usageItems.map((app, index) => ({
    app_id: app?.app_id,
    app_label: app?.display_name || "Unknown app",
    total_time: Number(app?.total_time || 0),
    fill: CHART_COLORS[index % CHART_COLORS.length],
  }))

  return (
    <Card>
      <CardHeader className="pb-0">
        <CardTitle>
          <span className="flex items-center gap-2">
            <span className="wrap-break-word whitespace-normal">{session?.session_name || "Unnamed session"}</span>
            {session?.deleted_at ? (
              <Badge variant="destructive" className="h-5 px-1.5 text-[10px]">In trash</Badge>
            ) : null}
          </span>
        </CardTitle>
        <CardDescription>Applications usage</CardDescription>
      </CardHeader>
      <CardContent>
        {chartData.length === 0 ? (
          <p className="text-muted-foreground text-sm">No apps usage data.</p>
        ) : (
          <>
            <div className="mx-auto h-65 w-full max-w-75">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Tooltip
                    cursor={false}
                    content={(
                      <StatisticsPieTooltip
                        formatDuration={formatDuration}
                        labelKey="app_label"
                        appIdKey="app_id"
                        showIcon
                      />
                    )}
                  />
                  <Pie
                    data={chartData}
                    dataKey="total_time"
                    nameKey="app_label"
                    strokeWidth={5}
                    labelLine={false}
                    label={({ payload, ...props }) => (
                      <text
                        cx={props.cx}
                        cy={props.cy}
                        x={props.x}
                        y={props.y}
                        textAnchor={props.textAnchor}
                        dominantBaseline={props.dominantBaseline}
                        fill="var(--foreground)"
                        className="text-xs"
                      >
                        {formatDuration(payload?.total_time)}
                      </text>
                    )}
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`${entry.app_label}-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2">
              {chartData.map((item, index) => (
                <div key={`${item.app_label}-${index}`} className="flex items-center gap-2 text-sm">
                  <span className="inline-block h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.fill }} />
                  <span className="text-muted-foreground wrap-break-word whitespace-normal">{item.app_label}</span>
                </div>
              ))}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
