Deletes a saved session by slug.

## Parameters

- `Authorization` (header, required): Bearer access token.
- `X-Device-Fingerprint` (header, required): Fingerprint of the current device.
- `session_slug` (path, required, string): Session slug.

## Example

Request:

```http
DELETE /session/by-slug/deep-work HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: your-device-fingerprint
```

Response:

```http
HTTP/1.1 204 No Content
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
