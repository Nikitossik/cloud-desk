## Parameters
- `Authorization` (header, required): Bearer access token for authentication.

- `session_slug` (path, required): Slugname of the session to retrieve.

## Example

Request:

```http
GET /session/work-session HTTP/1.1
Authorization: Bearer your-access-token
```

Successful Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ 
    "name": "Work Session", 
    "description": "Session for coding and meetings", 
    "slugname": "work-session", 
    "is_active": false, 
    "is_tracking": false, 
    "created_at": "2024-04-26T10:00:00Z", 
    "saved_at": "2024-04-26T11:00:00Z", 
    "restored_at": null, 
    "last_active_at": "2024-04-26T11:00:00Z" 
}
```

Error Response (when session not found):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "Session with the given name was not found" 
}
```
