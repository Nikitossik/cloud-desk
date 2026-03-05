import { http } from "@/shared/api/http-client"

export async function meRequest() {
  const { data } = await http.get("/user/me")
  return data
}

export async function updateMeRequest(payload) {
  const { data } = await http.patch("/user/me", payload)
  return data
}

export async function meSidebarRequest() {
  const { data } = await http.get("/user/me/sidebar")
  return data
}
