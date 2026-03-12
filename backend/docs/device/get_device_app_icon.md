Returns the PNG icon of an application by its `app_id` for the current device.

## Parameters

- Path:
  - `app_id` (UUID, required)
- Header (required):
  - `Authorization: Bearer <access-token>`
  - `X-Device-Fingerprint: <fingerprint>`

## Example

Request:

```http
GET /device/apps/9c9fbb9e-df4e-4b4a-8a40-58f98005a3ff/icon HTTP/1.1
Authorization: Bearer your-access-token
X-Device-Fingerprint: 5e84ab23-cf76-4ca8-9a08-92ef44e4f0a3
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: image/png

<binary png>
```
