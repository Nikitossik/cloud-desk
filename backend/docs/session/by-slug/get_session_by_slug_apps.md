Returns applications that belong to a session selected by slug.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_slug` (path, required, string): Session slug.

## Example

Request:

```http
GET /session/by-slug/deep-work/apps HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "app_id": "a6ff7780-c58a-4822-9b87-4900f146f6e5",
    "state_id": "f3790ee7-a99d-43fc-bf16-8954fc4e31c3",
    "name": "Code.exe",
    "is_active": true
  }
]
```
