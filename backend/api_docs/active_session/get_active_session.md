## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

## Example

Request:

```http
GET /active-session/ HTTP/1.1
Authorization: Bearer your-access-token
```

Successful response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ 
    "name": "Work Session", 
    "description": "Session for coding and meetings", 
    "slugname": "work-session", 
    "is_active": true, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:00:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": "2024-04-26T13:00:00Z" 
}
```

Error Response (when no active session exists):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "No active sessions at the moment"
}
```