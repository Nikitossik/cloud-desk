Updates fields of the currently authenticated user profile. You can send one or more fields in the request body.

## Parameters

- Header (required):
  - `Authorization: Bearer <access-token>`
- Body (JSON, required):
  - `name` (string, optional)
  - `surname` (string, optional)
  - `password` (string, optional)

## Example

Request:

```http
PATCH /user/me HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "name": "Johnny",
  "surname": "Doe"
}
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Johnny",
  "surname": "Doe",
  "email": "john.doe@example.com"
}
```
