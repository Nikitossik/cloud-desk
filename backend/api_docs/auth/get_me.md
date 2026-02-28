## Parameters

- `Authorization` (header, required): Bearer access token for authentication.

## Example

Request:

```http
GET /auth/me HTTP/1.1
Authorization: Bearer your-access-token
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ 
    "id": 1, 
    "name": "John", 
    "surname": "Doe", 
    "email": "john.doe@example.com" 
}
```