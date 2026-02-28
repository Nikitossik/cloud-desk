## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

## Example

Request:

```http
GET /active-session/apps HTTP/1.1
Authorization: Bearer your-access-token
```

Successful response:

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


Error Response (when no active session exists):

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{ 
    "detail": "No active sessions at the moment"
}
```