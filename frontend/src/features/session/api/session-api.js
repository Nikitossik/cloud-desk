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
export async function updateSessionByIdRequest(sessionId, payload) {
  const { data } = await http.patch(`/session/${sessionId}`, payload)
  return data
}

export async function deleteSessionByIdRequest(sessionId) {
  await http.delete(`/session/${sessionId}`)
}

export async function purgeSessionTrashRequest(payload) {
  const { data } = await http.post("/session/trash/purge", payload)
  return data
}

export async function startSessionByIdRequest(sessionId) {
  const { data } = await http.post(`/session/${sessionId}/start`)
  return data
}

export async function stopActiveSessionRequest() {
  const { data } = await http.post("/session/active/stop")
  return data
}

export async function restoreSessionByIdRequest(sessionId) {
  const { data } = await http.post(`/session/${sessionId}/restore`)
  return data
}
