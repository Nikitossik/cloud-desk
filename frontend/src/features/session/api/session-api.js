import { http } from "@/shared/api/http-client"

export async function getSessionBySlugRequest(sessionSlug) {
  const { data } = await http.get(`/session/by-slug/${sessionSlug}`)
  return data
}

export async function createSessionRequest({ name, description, start }) {
  const payload = {
    start,
  }

  if (typeof name === "string" && name.trim()) {
    payload.name = name.trim()
  }

  if (typeof description === "string" && description.trim()) {
    payload.description = description.trim()
  }

  const { data } = await http.post("/session", payload)
  return data
}
