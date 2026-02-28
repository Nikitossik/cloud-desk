## Parameters

- `form_data` (body, required): User login credentials. Must be a form with the following fields:

    - `username` (string, required): The user's email address. Must be a valid email format.

    - `password` (string, required): The user's password.

## Example

Request:

```http
POST /auth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=john.doe@example.com&password=securepassword123
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access_token": "your-access-token",
    "refresh_token": "your-refresh-token",
    "token_type": "bearer"
}
```