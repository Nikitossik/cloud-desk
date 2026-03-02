const ACCESS_TOKEN_KEY = "access_token"

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function setAccessToken(access_token) {
  if (access_token) {
    localStorage.setItem(ACCESS_TOKEN_KEY, access_token)
  }
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
}
