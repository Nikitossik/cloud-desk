## Parameters

- `Authorization` (header, required): Bearer access token for authentication.
- `X-Device-Fingerprint` (header, required): Device fingerprint used to resolve the current device context.

## Example

Request:

```http
GET /device/current/apps HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[ 
    { 
        "name": "Google Chrome", 
        "path": "C:\Program Files\Google\Chrome\Application\chrome.exe" }, 
        "cmdline": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --flag-switches-begin --some-flag"
    { 
        "name": "Visual Studio Code", 
        "path": "C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "cmdline": "\"C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe\""
    } 
]
```