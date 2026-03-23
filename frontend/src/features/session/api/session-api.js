import { http } from "@/shared/api/http-client"

export async function getSessionBySlugRequest(sessionSlug) {
  const { data } = await http.get(`/session/by-slug/${sessionSlug}`)
  return data
}

export async function getDeletedSessionsRequest() {
  const { data } = await http.get("/session", {
    params: {
      deleted_only: true,
    },
  })
  return data
}

export async function getSessionAppsBySlugRequest(sessionSlug) {
  const { data } = await http.get(`/session/by-slug/${sessionSlug}/apps`)
  return data
}

export async function createSessionRequest({ name, description, start }) {
  const payload = {
    name,
    description,
    start,
  }

  const { data } = await http.post("/session", payload)
  return data
}

export async function updateActiveSessionRequest(payload) {
  const { data } = await http.patch("/session/active", payload)
  return data
}

export async function updateSessionByIdRequest(sessionId, { name, description }) {
  const payload = {
    name,
    description,
  }

  const { data } = await http.patch(`/session/${sessionId}`, payload)
  return data
}

export async function updateSessionBySlugRequest(sessionSlug, payload) {
  const { data } = await http.patch(`/session/by-slug/${sessionSlug}`, payload)
  return data
}

export async function deleteActiveSessionRequest() {
  await http.delete("/session/active")
}

export async function deleteSessionByIdRequest(sessionId) {
  await http.delete(`/session/${sessionId}`)
}

export async function startSessionByIdRequest(sessionId) {
  const { data } = await http.post(`/session/${sessionId}/start`)
  return data
}

export async function stopActiveSessionRequest() {
  const { data } = await http.post("/session/active/stop")
  return data
}

export async function restoreActiveSessionRequest() {
  const { data } = await http.post("/session/active/restore")
  return data
}

export async function restoreSessionByIdRequest(sessionId) {
  const { data } = await http.post(`/session/${sessionId}/restore`)
  return data
}
