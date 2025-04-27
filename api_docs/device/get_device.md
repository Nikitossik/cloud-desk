
## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

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

{ 
    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851", 
    "mac_address": "00:1A:2B:3C:4D:5E", 
    "os_name": "Windows", 
    "os_release": "10", 
    "os_release_ver": "10.0.19045", 
    "architecture": "AMD64", 
    "created_at": "2024-04-26T12:34:56.789Z" 
}
```
