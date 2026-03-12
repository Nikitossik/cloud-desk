Returns local machine data collected from the current runtime environment.

## Parameters

- No authentication, query, or body parameters are required.

## Example

Request:

```http
GET /device/local HTTP/1.1
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "display_name": "Work Laptop",
  "mac_address": "00:11:22:33:44:55",
  "os_name": "Windows",
  "os_release": "11",
  "os_release_ver": "10.0.22631",
  "architecture": "AMD64"
}
```
