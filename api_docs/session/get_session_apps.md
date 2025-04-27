## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

- `session_slug` (path, required): Slugname of the session whose applications should be retrieved.

## Example

Request:

```http
GET /session/work-session/apps HTTP/1.1
Authorization: Bearer your-access-token
```

Successful Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[ 
    { 
        "name": "Google Chrome", 
        "exe": "C:\Program Files\Google\Chrome\Application\chrome.exe", 
        "cmdline": ""C:\Program Files\Google\Chrome\Application\chrome.exe"", 
        "is_active": true, 
        "usage_periods": [ 
            { 
                "started_at": "2024-04-26T10:00:00Z", 
                "ended_at": "2024-04-26T11:00:00Z" 
            } 
            ], 
        "total_seconds": 3600 
    } 
]
```

Error Response (when session not found):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "Session with the given name was not found" 
}
```