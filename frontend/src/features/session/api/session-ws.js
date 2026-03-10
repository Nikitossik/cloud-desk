export function connectActiveSessionAppsWebSocket({
  token,
  deviceFingerprint,
}) {
  const apiBase = import.meta.env.VITE_API_URL ?? "http://localhost:8000"
  const wsBase = apiBase.replace(/^http/i, "ws")
  const wsUrl = `${wsBase}/ws/session/active/apps?token=${encodeURIComponent(token || "")}&device_fingerprint=${encodeURIComponent(deviceFingerprint || "")}`

  return new WebSocket(wsUrl)
}
