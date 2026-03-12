Updates a saved session by UUID.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_id` (path, required, UUID): Session identifier.
- Body (JSON, required):
  - `name` (string, optional)
  - `description` (string, optional)

## Example

Request:

```http
PATCH /session/b6f7f6f4-c355-4702-b8f9-8fd78016068a HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "name": "Deep Work Updated"
}
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
  "name": "Deep Work Updated",
  "description": "Focus block",
  "slugname": "deep-work-updated",
  "is_active": false,
  "created_at": "2026-03-12T10:00:00Z",
  "saved_at": null,
  "restored_at": null,
  "last_active_at": null
}
```
