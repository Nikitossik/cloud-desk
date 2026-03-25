Creates a new session for the current device.

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
POST /session/ HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "name": "Deep Work",
  "description": "Focus block",
  "start": true
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
  "name": "Deep Work",
  "description": "Focus block",
  "slugname": "deep-work",
  "is_active": true,
  "created_at": "2026-03-12T10:00:00Z",
  "last_restored_at": null,
  "last_active_at": "2026-03-12T10:00:00Z"
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
