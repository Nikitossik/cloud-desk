Authenticates a user with form credentials and returns an access token. If device confirmation is required, the API returns `409` with a `resolution_token`; otherwise a `refresh_token` is set as HttpOnly cookie.

## Parameters

- Note for Swagger: if this fingerprint already belongs to a known device, pass it in `client_id`; otherwise device resolution flow will be triggered.

- Header (optional):
    - `X-Device-Fingerprint` (string)
- Body (`application/x-www-form-urlencoded`, required):
    - `username` (string, required)
    - `password` (string, required)

## Example

Request:

```http
POST /auth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
X-Device-Fingerprint: 5e84ab23-cf76-4ca8-9a08-92ef44e4f0a3

username=john.doe@example.com&password=securepassword123
```

Successful response:

```http
HTTP/1.1 200 OK
Set-Cookie: refresh_token=<token>; HttpOnly; Path=/auth; SameSite=Lax
Content-Type: application/json

{
    "access_token": "your-access-token",
    "token_type": "bearer"
}
```

Device resolution required response:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
    "detail": {
        "code": "device_resolution_required",
        "resolution_token": "your-resolution-token"
    }
}
```