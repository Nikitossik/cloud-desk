## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

## Example

Request:

```http
DELETE /active-session/ HTTP/1.1
Authorization: Bearer your-access-token
```

Successful response:

```http
HTTP/1.1 204 No Content
```

Error Response (when no active session exists):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "No active sessions at the moment"
}
```