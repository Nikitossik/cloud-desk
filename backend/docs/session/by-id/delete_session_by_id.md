Deletes a saved session by UUID.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_id` (path, required, UUID): Session identifier.

## Example

Request:

```http
DELETE /session/b6f7f6f4-c355-4702-b8f9-8fd78016068a HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 204 No Content
```
