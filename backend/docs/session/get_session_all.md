Returns all saved sessions for the current authenticated device.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.

## Example

Request:

```http
GET /session/ HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
    "name": "Deep Work",
    "description": "Focus block",
    "slugname": "deep-work",
    "is_active": false,
    "created_at": "2026-03-12T10:00:00Z",
    "saved_at": null,
    "restored_at": null,
    "last_active_at": null
  }
]
```
