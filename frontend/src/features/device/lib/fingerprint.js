const DEVICE_FINGERPRINT_KEY = "device_fingerprint"

function generateFingerprint() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID()
  }

  return `${Date.now()}-${Math.random().toString(36).slice(2, 12)}`
}

export function getOrCreateDeviceFingerprint() {
  let fingerprint = localStorage.getItem(DEVICE_FINGERPRINT_KEY)

  if (!fingerprint) {
    fingerprint = generateFingerprint()
    localStorage.setItem(DEVICE_FINGERPRINT_KEY, fingerprint)
  }

  return fingerprint
}

export function getDeviceFingerprint() {
  return localStorage.getItem(DEVICE_FINGERPRINT_KEY)
}

export function ensureDeviceFingerprint() {
  return getOrCreateDeviceFingerprint()
}

export function setDeviceFingerprint(fingerprint) {
  if (!fingerprint) return
  localStorage.setItem(DEVICE_FINGERPRINT_KEY, fingerprint)
}
