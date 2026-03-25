Returns sessions for the current authenticated device.

By default, returns non-deleted sessions. Use `deleted_only=true` to return only sessions moved to trash.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `deleted_only` (query, optional, boolean, default: `false`):
  - `false` → return regular (not deleted) sessions.
  - `true` → return only deleted sessions (trash).

## Example

Request:

```http
GET /session/ HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Request (only deleted):

```http
GET /session/?deleted_only=true HTTP/1.1
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
    "last_restored_at": null,
    "last_active_at": null,
    "last_deleted_at": null
  }
]
```
