Updates a saved session by slug.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_slug` (path, required, string): Session slug.
- Body (JSON, required):
  - `name` (string, optional)
  - `description` (string, optional)

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
  "saved_at": null,
  "restored_at": null,
  "last_active_at": null
}
```
