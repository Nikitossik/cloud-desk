Binds a selected existing device to a new fingerprint and completes login. Requires a valid resolution token and sets refresh token cookie on success.

## Parameters

- Authorization:
  - Resolution token (used by dependency resolver)
- Body (JSON, required):
  - `target_device_id` (UUID string, required)
  - `new_fingerprint` (string, required)

## Example

Request:

```http
POST /auth/device/resolve/rebind HTTP/1.1
Authorization: Bearer <resolution-token>
Content-Type: application/json

{
  "target_device_id": "7d44a5f2-6096-4f38-a2c0-7cab50b0f931",
  "new_fingerprint": "3de0f748-2ca2-4ca6-b86f-0ea9a7449b4f"
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