## Parameters
- `Authorization` (header, required): Bearer access token for authentication.

- `device_session` (body, required): Data for the new session.

    - `name` (string, optional): Name of the session. If omitted or empty, a slugified name will be automatically generated.

    - `description` (string, optional): Description of the session.

    - `activate` (boolean, optional): Whether to activate the session immediately.

    - `enable_tracking` (boolean, optional): Whether to enable application tracking.

## Example

Request:

```http
POST /session/ HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "", 
    "description": "New working session", 
    "activate": true, 
    "enable_tracking": true 
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "brave-sky-dragon", 
    "description": "New working session", 
    "slugname": "brave-sky-dragon", 
    "is_active": true, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:00:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": "2024-04-26T12:00:00Z" 
}
```
