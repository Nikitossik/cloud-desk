Creates or binds a new device fingerprint for the user during device-resolution flow. Requires a valid resolution token and sets refresh token cookie on success.

## Parameters

- Authorization:
  - Resolution token (used by dependency resolver)
- Body (JSON, required):
  - `new_fingerprint` (string, required)
  - `display_name` (string, optional)

## Example

Request:

```http
POST /auth/device/resolve/create HTTP/1.1
Authorization: Bearer <resolution-token>
Content-Type: application/json

{
  "new_fingerprint": "3de0f748-2ca2-4ca6-b86f-0ea9a7449b4f",
  "display_name": "Home PC"
}
```

Response:

```http
HTTP/1.1 200 OK
Set-Cookie: refresh_token=<token>; HttpOnly; Path=/auth; SameSite=Lax
Content-Type: application/json

{
  "access_token": "your-access-token",
  "token_type": "bearer"
}
```