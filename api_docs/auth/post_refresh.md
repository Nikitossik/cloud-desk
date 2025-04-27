## Parameters

- `X-Refresh-Token` (header, required): The user's refresh token used to obtain a new access token.

## Example

Request:

```http
POST /auth/refresh HTTP/1.1
X-Refresh-Token: your-refresh-token
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ 
    "access_token": "new-access-token", 
    "refresh_token": "new-refresh-token", 
    "token_type": "bearer" 
}
```