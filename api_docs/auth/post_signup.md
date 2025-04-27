## Parameters

- `user` (body, required): Data of a new user. Must be a JSON object with the following properties:

    - `name` (string, required): The user's first name. Must be a string of maximum 20 characters.

    - `surname` (string, required): The user's last name. Must be a string of maximum 20 characters.

    - `email` (string, required): The user's email address. Must be a valid email format.

    - `password` (string, required): The user's password. Must be at least 6 characters long.


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