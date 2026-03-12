Returns all devices linked to the currently authenticated user.

## Parameters

- Header (required):
  - `Authorization: Bearer <access-token>`

## Example

Request:

```http
GET /device/ HTTP/1.1
Authorization: Bearer your-access-token
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
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
    "last_seen_at": "2026-03-10T10:30:00Z"
  }
]
```
