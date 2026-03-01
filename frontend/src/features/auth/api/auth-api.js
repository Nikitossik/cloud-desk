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

export async function refreshRequest(refreshToken) {
  const { data } = await http.post(
    "/auth/refresh",
    {},
    {
      skipAuthAttach: true,
      skipAuthRefresh: true,
      headers: {
        "X-Refresh-Token": refreshToken,
      },
    }
  )

  return data
}

export async function meRequest(accessToken) {
  const { data } = await http.get("/user/me", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  return data
}

export async function updateMeRequest(payload) {
  const { data } = await http.patch("/user/me", payload)
  return data
}
