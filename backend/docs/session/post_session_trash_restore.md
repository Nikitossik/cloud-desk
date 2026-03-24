Restores deleted sessions from trash for the current authenticated device.

Payload format is the same as `/session/trash/purge`:

- `all: true` — restores all deleted sessions.
- `session_ids: [...]` — restores only selected deleted sessions.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.

## Example

Request:

```http
POST /session/trash/restore HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "all": false,
  "session_ids": [
    "b6f7f6f4-c355-4702-b8f9-8fd78016068a"
  ]
}
```

Response:

```http
HTTP/1.1 204 No Content
```
