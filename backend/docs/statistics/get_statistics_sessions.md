Returns aggregated session usage statistics for the current authenticated device.

For each session, the response contains:

- `last_deleted_at`: timestamp if session is in trash, otherwise `null`
- `start_count`: number of times the session was started
- `restore_count`: number of times the session was restored
- `total_active_time`: total active time in seconds (computed from STARTED/STOPPED events)
- `usage`: grouped by application with `total_time` in seconds.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `all_sessions` (query, optional, default `true`):
  - `true` — include all sessions (including sessions in trash)
  - `false` — include only sessions not in trash

## Example

Request:

```http
GET /statistics/sessions?all_sessions=true HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "session_id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
    "session_name": "Deep Work",
    "last_deleted_at": null,
    "start_count": 12,
    "restore_count": 4,
    "total_active_time": 9000,
    "usage": [
      {
        "app_id": "cc7b5703-87a2-47fc-8ef6-f4279d0c02dd",
        "display_name": "Chrome",
        "total_time": 5400
      },
      {
        "app_id": "7fd3a7b1-18df-4f32-a279-8f2ebebf4ffc",
        "display_name": "PyCharm",
        "total_time": 3600
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
