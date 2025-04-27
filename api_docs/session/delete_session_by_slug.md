## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

- `session_slug` (path, required): Slugname of the session to delete.

## Example

Request:

```http
DELETE /session/work-session HTTP/1.1
Authorization: Bearer your-access-token
```

Successful Response:

```http
HTTP/1.1 204 No Content
```

Error Response (when session not found):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "Session with the given name was not found" 
}
```