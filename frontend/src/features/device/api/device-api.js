import { http } from "@/shared/api/http-client"
import { getDeviceFingerprint } from "@/features/device/lib/fingerprint"

export async function getCurrentDeviceRequest() {
  const fingerprint = getDeviceFingerprint()
  const { data } = await http.get("/device/current", {
    headers: fingerprint ? { "X-Device-Fingerprint": fingerprint } : undefined,
  })
  return data
}

export async function updateCurrentDeviceRequest(displayName) {
  const fingerprint = getDeviceFingerprint()
  const { data } = await http.patch("/device/current", {
    display_name: displayName,
  }, {
    headers: fingerprint ? { "X-Device-Fingerprint": fingerprint } : undefined,
  })

  return data
}

export async function meDevicesRequest() {
  const { data } = await http.get("/user/me/devices")
  return data
}

export async function detectLocalDeviceRequest() {
  const { data } = await http.get("/device/local", {
    skipAuthAttach: true,
    skipAuthRefresh: true,
  })
  return data
}
