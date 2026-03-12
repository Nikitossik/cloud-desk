Cancels the current device-resolution flow. Optionally removes user account created during unfinished signup flow.

## Parameters

- Authorization:
  - Resolution token (used by dependency resolver)
- Body (JSON, optional):
  - `remove_user` (boolean, optional, default: `false`)

## Example

Request:

```http
POST /auth/device/resolve/cancel HTTP/1.1
Authorization: Bearer <resolution-token>
Content-Type: application/json

{
  "remove_user": true
}
```

Response:

```http
HTTP/1.1 204 No Content
```
