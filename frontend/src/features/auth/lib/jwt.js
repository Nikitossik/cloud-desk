export function parseJwtPayload(token) {
  try {
    if (!token) return null

    const base64Url = token.split(".")[1]
    if (!base64Url) return null

    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/")
    const json = decodeURIComponent(
      atob(base64)
        .split("")
        .map((char) => `%${(`00${char.charCodeAt(0).toString(16)}`).slice(-2)}`)
        .join("")
    )

    return JSON.parse(json)
  } catch {
    return null
  }
}

export function getExpMs(token) {
  const payload = parseJwtPayload(token)
  if (!payload?.exp) return null
  return payload.exp * 1000
}

export function isExpired(token, skewMs = 0) {
  const expMs = getExpMs(token)
  if (!expMs) return true
  return Date.now() + skewMs >= expMs
}
