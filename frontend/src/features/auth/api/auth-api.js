import { http } from "@/shared/api/http-client"

export async function loginRequest(email, password) {
  const body = new URLSearchParams()
  body.append("username", email)
  body.append("password", password)

  const { data } = await http.post("/auth/token", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  })

  return data
}

export async function signupRequest({ name, surname, email, password }) {
  const { data } = await http.post("/auth/signup", {
    name,
    surname,
    email,
    password,
  })

  return data
}

export async function refreshRequest() {
  const { data } = await http.post(
    "/auth/refresh",
    {},
    {
      skipAuthAttach: true,
      skipAuthRefresh: true,
    }
  )

  return data
}

export async function getResolutionDevicesRequest(resolutionToken) {
  const { data } = await http.post(
    "/auth/device/resolve/devices",
    {},
    {
      headers: { "X-Resolution-Token": resolutionToken },
      skipAuthAttach: true,
      skipAuthRefresh: true,
    }
  )

  return data
}

export async function resolveDeviceRebindRequest({
  resolutionToken,
  targetDeviceId,
  newFingerprint,
}) {
  const { data } = await http.post(
    "/auth/device/resolve/rebind",
    {
      target_device_id: targetDeviceId,
      new_fingerprint: newFingerprint,
    },
    {
      headers: { "X-Resolution-Token": resolutionToken },
      skipAuthAttach: true,
      skipAuthRefresh: true,
    }
  )

  return data
}

export async function resolveDeviceCreateRequest({
  resolutionToken,
  newFingerprint,
  displayName,
}) {
  const { data } = await http.post(
    "/auth/device/resolve/create",
    {
      new_fingerprint: newFingerprint,
      display_name: displayName,
    },
    {
      headers: { "X-Resolution-Token": resolutionToken },
      skipAuthAttach: true,
      skipAuthRefresh: true,
    }
  )

  return data
}

export async function cancelDeviceResolutionRequest({
  resolutionToken,
  removeUser,
}) {
  await http.post(
    "/auth/device/resolve/cancel",
    {
      remove_user: removeUser,
    },
    {
      headers: { "X-Resolution-Token": resolutionToken },
      skipAuthAttach: true,
      skipAuthRefresh: true,
    }
  )
}
