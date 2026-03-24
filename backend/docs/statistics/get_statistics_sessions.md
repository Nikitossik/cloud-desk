Returns aggregated session usage statistics for the current authenticated device.

For each session, the response contains usage grouped by application with `total_time` in seconds.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.

## Example

Request:

```http
GET /statistics/sessions HTTP/1.1
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
