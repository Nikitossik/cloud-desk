import { Cell, Label, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { SessionAppIcon } from "@/pages/session/components/session-app-icon"
import { StatisticsPieTooltip } from "@/pages/statistics/components/statistics-pie-tooltip"
import { Trash2 } from "lucide-react"

const CHART_COLORS = [
  "var(--chart-1)",
  "var(--chart-2)",
  "var(--chart-3)",
  "var(--chart-4)",
  "var(--chart-5)",
]

export function StatisticsSessionAppCard({ app, formatDuration, usage }) {
  const usageItems = Array.isArray(usage) ? usage : []
  const chartData = usageItems.map((item, index) => ({
    session_id: item?.session_id,
    session_name: item?.session_name || "Unknown session",
    last_deleted_at: item?.last_deleted_at || null,
    total_time: Number(item?.total_time || 0),
    fill: item?.last_deleted_at ? "var(--muted-foreground)" : CHART_COLORS[index % CHART_COLORS.length],
  }))
  const totalUsage = chartData.reduce((sum, item) => sum + item.total_time, 0)

  return (
    <Card className="flex flex-col">
      <CardHeader className="pb-0">
        <CardTitle>
          <span className="flex items-center gap-2">
            <SessionAppIcon appId={app?.app_id} appName={app?.display_name || "Unknown app"} />
            <span className="wrap-break-word whitespace-normal">{app?.display_name || "Unknown app"}</span>
          </span>
        </CardTitle>
        <CardDescription>Session usage distribution</CardDescription>
      </CardHeader>

      <CardContent>
        {chartData.length > 0 ? (
          <>
            <div className="mx-auto h-65 w-full max-w-75">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Tooltip
                    cursor={false}
                    content={(
                      <StatisticsPieTooltip
                        formatDuration={formatDuration}
                        labelKey="session_name"
                        deletedAtKey="last_deleted_at"
                      />
                    )}
                  />
                  <Pie
                    data={chartData}
                    dataKey="total_time"
                    nameKey="session_name"
                    innerRadius={64}
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
                      <Cell key={`${entry.session_name}-${index}`} fill={entry.fill} />
                    ))}
                    <Label
                      content={({ viewBox }) => {
                        if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                          return (
                            <text
                              x={viewBox.cx}
                              y={viewBox.cy}
                              textAnchor="middle"
                              dominantBaseline="middle"
                            >
                              <tspan
                                x={viewBox.cx}
                                y={viewBox.cy}
                                className="fill-foreground text-sm font-bold"
                              >
                                {formatDuration(totalUsage)}
                              </tspan>
                              <tspan
                                x={viewBox.cx}
                                y={(viewBox.cy || 0) + 18}
                                className="fill-muted-foreground text-xs"
                              >
                                Total usage
                              </tspan>
                            </text>
                          )
                        }

                        return null
                      }}
                    />
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2">
              {chartData.map((item, index) => (
                <div key={String(item.session_id || `${item.session_name}-${index}`)} className="flex items-center gap-2 text-sm">
                  <span className="inline-block h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.fill }} />
                  <span className="text-muted-foreground">{item.session_name}</span>
                  {item.last_deleted_at ? <Trash2 className="text-destructive size-3.5" /> : null}
                </div>
              ))}
            </div>
          </>
        ) : (
          <p className="text-muted-foreground text-sm">No session usage data.</p>
        )}
      </CardContent>
    </Card>
  )
}
