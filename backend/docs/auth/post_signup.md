Creates a new user account with email and password. If a user with the same email already exists, the API returns `422`.

## Parameters

- Body (JSON, required):
    - `name` (string, required)
    - `surname` (string, required)
    - `email` (string, required, valid email)
    - `password` (string, required)

## Example

Request:

```http
POST /auth/signup HTTP/1.1
Content-Type: application/json

{
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
}
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