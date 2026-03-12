Returns the profile of the currently authenticated user. Requires a valid access token.

## Parameters

- Header (required):
  - `Authorization: Bearer <access-token>`

## Example

Request:

```http
GET /user/me HTTP/1.1
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
