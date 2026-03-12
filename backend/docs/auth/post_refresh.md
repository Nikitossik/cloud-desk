Refreshes the access token using `refresh_token` from cookies. If cookie is missing or invalid, the API returns `401`.

## Parameters

- Cookie (required):
    - `refresh_token` (string)

## Example

Request:

```http
POST /auth/refresh HTTP/1.1
Cookie: refresh_token=your-refresh-token
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access_token": "new-access-token",
    "token_type": "bearer"
}
```