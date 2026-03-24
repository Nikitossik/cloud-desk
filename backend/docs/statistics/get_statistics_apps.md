Returns aggregated application usage statistics for the current authenticated device.

For each application, the response contains:

- `total_time`: total usage in seconds across all sessions.
- `usage`: usage grouped by session, each item with:
  - `session_id`: session identifier
  - `session_name`: session title
  - `deleted_at`: timestamp if session is in trash, otherwise `null`
  - `total_time`: usage in seconds

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
        "session_id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
        "session_name": "Deep Work",
        "deleted_at": null,
        "total_time": 5400
      },
      {
        "session_id": "e5306f2a-4ce2-426c-8ab8-7ad2b7b4c12a",
        "session_name": "Research",
        "deleted_at": "2026-03-24T11:05:00Z",
        "total_time": 1800
      }
    ]
  }
]
```
