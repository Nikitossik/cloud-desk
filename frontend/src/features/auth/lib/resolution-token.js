export function extractResolutionToken(error) {
  const detail = error?.response?.data?.detail
  if (!detail || typeof detail !== "object") return ""
  if (detail.code !== "device_resolution_required") return ""
  return detail.resolution_token || ""
}

export function isResolutionTokenProblem(error) {
  const statusCode = error?.response?.status
  if (statusCode !== 401) return false

  const detail = error?.response?.data?.detail
  const detailText =
    typeof detail === "string"
      ? detail
      : typeof detail?.message === "string"
        ? detail.message
        : ""

  const normalized = detailText.toLowerCase()

  return (
    normalized.includes("expired resolution token") ||
    normalized.includes("invalid resolution token") ||
    normalized.includes("missing x-resolution-token")
  )
}
