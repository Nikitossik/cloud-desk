Returns apps for the active session.

> Note: this REST endpoint is currently not exposed in `app/routes/session.py`. If enabled in the future, use the contract below.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.

## Example

Request:

```http
GET /session/active/apps HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response (example shape based on `FullApplicationOut`):

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "name": "Google Chrome",
    "exe": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "cmdline": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\"",
    "is_active": true,
    "usage_periods": [
      {
        "started_at": "2026-03-12T09:00:00Z",
        "ended_at": "2026-03-12T09:30:00Z"
      }
    ]
  }
]
```

## Unsupported OS

If the current device OS is not supported, the endpoint returns:

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "detail": {
    "code": "DEVICE_OS_NOT_SUPPORTED",
    "message": "This feature is available only on desktop Windows devices."
  }
}
```
