## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

- `save_usage` (query, optional, default=True): Whether to save usage periods before disabling tracking.

## Example

Request:

```http
POST /active-session/disable-tracking?save_usage=true HTTP/1.1
Authorization: Bearer your-access-token
```

Successful response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "Work Session", 
    "description": "Session for coding and meetings", 
    "slugname": "work-session", 
    "is_active": true, 
    "is_tracking": false, 
    "created_at": "2024-04-26T12:00:00Z", 
    "saved_at": "2024-04-26T13:45:00Z", 
    "restored_at": null, 
    "last_active_at": "2024-04-26T13:45:00Z" 
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