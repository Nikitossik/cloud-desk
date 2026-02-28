## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

- `session_slug` (path, required): Slugname of the session to clone.

- `device_session` (body, required): Data for the new session.

    - `name` (string, optional): Name for the new session. If omitted or empty, a slugified name will be generated automatically.

    - `description` (string, optional): Description of the new session.

    - `activate` (boolean, optional): Whether to activate the new session immediately.

    - `enable_tracking` (boolean, optional): Whether to enable application tracking.

## Example

Request:

```http
POST /session/work-session/clone HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "", 
    "description": "Cloned work session", 
    "activate": true, 
    "enable_tracking": true 
}
```

Successful Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "silent-night-owl", 
    "description": "Cloned work session", 
    "slugname": "silent-night-owl", 
    "is_active": true, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:30:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": "2024-04-26T12:30:00Z" 
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