import { http } from "@/shared/api/http-client"

export async function getStatisticsAppsRequest() {
  const { data } = await http.get("/statistics/apps")
  return data
}

export async function getStatisticsSessionsRequest({ allSessions = true } = {}) {
  const { data } = await http.get("/statistics/sessions", {
    params: { all_sessions: allSessions },
  })
  return data
}
