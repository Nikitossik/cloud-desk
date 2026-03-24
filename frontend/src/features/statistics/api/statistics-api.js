import { http } from "@/shared/api/http-client"

export async function getStatisticsAppsRequest() {
  const { data } = await http.get("/statistics/apps")
  return data
}

export async function getStatisticsSessionsRequest() {
  const { data } = await http.get("/statistics/sessions")
  return data
}
