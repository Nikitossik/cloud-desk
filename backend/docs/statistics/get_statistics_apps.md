Returns aggregated application usage statistics for the current authenticated device.

For each application, the response contains:

- `total_time`: total usage in seconds across all sessions.
- `usage`: usage grouped by session, each item with `total_time` in seconds.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.

## Example

Request:

```http
GET /statistics/apps HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "app_id": "cc7b5703-87a2-47fc-8ef6-f4279d0c02dd",
    "display_name": "Chrome",
    "total_time": 7200,
    "usage": [
      {
        "session_name": "Deep Work",
        "total_time": 5400
      },
      {
        "session_name": "Research",
        "total_time": 1800
      }
    ]
  }
]
```
