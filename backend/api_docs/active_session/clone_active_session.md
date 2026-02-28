## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

- `device_session` (body, required): Data for the new session.

    - `name` (string, optional): Name for the new session. If omitted or empty, a slugified name will be generated automatically.

    - `description` (string, optional): Description of the new session.

    - `activate` (boolean, optional): Whether to activate the new session immediately.

    - `enable_tracking` (boolean, optional): Whether to enable application tracking.

## Examples

**Empty name provided**

Request:

```http
POST /active-session/clone HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "", 
    "description": "Cloned session from active one", 
    "activate": true, 
    "enable_tracking": false 
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "brave-sky-dragon", 
    "description": "Cloned session from active one", 
    "slugname": "brave-sky-dragon", 
    "is_active": true, 
    "is_tracking": false, 
    "created_at": "2024-04-26T12:30:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": "2024-04-26T13:15:00Z" 
}
```

**Not empty name provided**

Request:

```http
POST /active-session/clone HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "active session clone", 
    "description": "Cloned session from active one", 
    "activate": true, 
    "enable_tracking": false 
}
```

Successful response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "active session clone", 
    "description": "Cloned session from active one", 
    "slugname": "active-session-clone", 
    "is_active": true, 
    "is_tracking": false, 
    "created_at": "2024-04-26T12:30:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": "2024-04-26T13:15:00Z" 
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