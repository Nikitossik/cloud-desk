Updates a saved session by slug.

Supports both regular field updates and trash/restore flow via `is_deleted`.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_slug` (path, required, string): Session slug.
- Body (JSON, required):
  - `name` (string, optional)
  - `description` (string, optional)
  - `is_deleted` (boolean, optional):
    - `true` → move session to trash.
    - `false` → restore session from trash.

If `is_deleted` is provided, it controls soft-delete state.

## Example

Request:

```http
PATCH /session/by-slug/deep-work HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "description": "Updated description"
}
```

Request (move to trash):

```http
PATCH /session/by-slug/deep-work HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "is_deleted": true
}
```

Request (restore from trash):

```http
PATCH /session/by-slug/deep-work HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "is_deleted": false
}
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
  "name": "Deep Work",
  "description": "Updated description",
  "slugname": "deep-work",
  "is_active": false,
  "created_at": "2026-03-12T10:00:00Z",
  "last_restored_at": null,
  "last_active_at": null,
  "last_deleted_at": null
}
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
