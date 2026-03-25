Returns aggregated sidebar data for the current user: devices with current marker and support flags, non-deleted sessions list, and deleted sessions count.

`sessions` contains only sessions that are not deleted (`last_deleted_at is null`).

Each device in `devices` contains:

- `is_supported_os`: `true` only for desktop Windows devices.
- `unsupported_reason`: optional message when the device OS is not supported.

## Parameters

- Header (required):
  - `Authorization: Bearer <access-token>`
  - `X-Device-Fingerprint: <fingerprint>`

## Example

Request:

```http
GET /user/me/sidebar HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: 5e84ab23-cf76-4ca8-9a08-92ef44e4f0a3
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "devices": [
    {
      "id": "7d44a5f2-6096-4f38-a2c0-7cab50b0f931",
      "fingerprint": "5e84ab23-cf76-4ca8-9a08-92ef44e4f0a3",
      "display_name": "Work Laptop",
      "mac_address": "00:11:22:33:44:55",
      "os_name": "Windows",
      "os_release": "11",
      "os_release_ver": "10.0.22631",
      "architecture": "AMD64",
      "created_at": "2026-03-10T10:00:00Z",
      "last_seen_at": "2026-03-10T10:30:00Z",
      "is_current": true,
      "is_supported_os": true,
      "unsupported_reason": null
    }
  ],
  "sessions": [
    {
      "slugname": "deep-work",
      "name": "Deep work",
      "is_active": true
    }
  ],
  "deleted_sessions_count": 2
}
```

If the current device OS is not supported, this endpoint still returns `200` with `devices[].is_supported_os = false` for the current device so the client can show graceful feedback.
