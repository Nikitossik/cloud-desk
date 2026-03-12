Clones the current active session into a new session.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- Body (JSON, required):
  - `name` (string, optional)
  - `description` (string, optional)
  - `start` (boolean, optional, default `true`)

## Example

Request:

```http
POST /session/active/clone HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "name": "Active Clone",
  "description": "Created from active session",
  "start": false
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "c99a27f9-078d-4a93-b8ca-3df36d8ea6c9",
  "name": "Active Clone",
  "description": "Created from active session",
  "slugname": "active-clone",
  "is_active": false,
  "created_at": "2026-03-12T10:10:00Z",
  "saved_at": null,
  "restored_at": null,
  "last_active_at": null
}
```
