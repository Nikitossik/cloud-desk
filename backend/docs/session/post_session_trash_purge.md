Permanently deletes sessions from trash for the current authenticated device.

Use exactly one mode:
- Provide `all: true` to clear the whole trash.
- Provide `session_ids` to delete only selected deleted sessions.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- Body (JSON, required):
  - `all` (boolean, optional): when `true`, purge all deleted sessions.
  - `session_ids` (array of UUID, optional): selected deleted session IDs to purge.

## Example

Request (purge selected):

```http
POST /session/trash/purge HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "session_ids": [
    "b6f7f6f4-c355-4702-b8f9-8fd78016068a",
    "19b9df15-91fc-4f1f-b139-8f3e4fefee0d"
  ]
}
```

Request (purge all):

```http
POST /session/trash/purge HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
Content-Type: application/json

{
  "all": true
}
```

Response:

```http
HTTP/1.1 204 No Content
```
