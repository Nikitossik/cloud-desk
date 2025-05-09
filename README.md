# cloud-desk

CloudDesk API is a backend application for managing user sessions, tracking application usage, and restoring working environments. Each session represents a list of open applications, and users can clone, activate, restore, and monitor their sessions. Currently, the system is designed to work only on Windows environments.

## Technologies

- Python 3.11+
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite
- Windows 10/11 (current supported OS)

## Features

- User registration and authentication (JWT-based)
- Device registration and management
- Creation, activation, cloning, and deletion of sessions
- Enabling and disabling application tracking within sessions
- Session restoration with reopening tracked applications
- Application usage time statistics

## Project structure

``` 
.
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── main.py
├── api_docs/
│   ├── active_session/
│   ├── auth/
│   ├── device/
│   ├── session/
│   └── app_docs.py
├── app/
│   ├── config.py
│   ├── database.py
│   ├── dependencies/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── tracking/
│   └── utils/
├── tests/
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Windows 10 or 11

### Installation

1. Clone the repository and go to the root folder:

```
git clone https://github.com/your-username/cloud-desk-api.git
cd cloud-desk-api
```

2. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
python -m pip install -r requirements.txt
```

4. Set up the environment variables (you can use your own secrets):

```
cp .env.example .env
```

5. Run the application:

```
fastapi dev main.py
```

Interactive documentation will be available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Additionally, detailed examples of API requests and responses are available in the [api_docs](./api_docs) directory.

## Examples

### Register a new user

This example creates a John Doe user with email john.doe@example.com and password securepassword123.

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

### Create a new active session

Let's say the user wants to create a new session that will be active and tracked, meaning that he wants to track how much time he's spent in different applications during the session. 

Request:

```http
POST /session/ HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "", 
    "description": "New working session", 
    "activate": true, 
    "enable_tracking": true 
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "brave-sky-dragon", 
    "description": "New working session", 
    "slugname": "brave-sky-dragon", 
    "is_active": true, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:00:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": null 
}
```

> This example creates a new session with an autogenerated name and slugname.
> You can specify your own session name and the slug will be generated according to it.  
> Sessions become active and tracked by default unless "activate" and "enable_tracking" are set to False.  
> If the new session becomes active, the previous one becomes deactivated and saves the applications usage time if it was tracked. 


### Clone active session

Imagine that the user wants a new active clone of that session - so all applications and their states (opened or closed) will be saved to that clone. We can make a clone like this:

Request:

```http
POST /active-session/clone HTTP/1.1
Authorization: Bearer your-access-token
Content-Type: application/json

{ 
    "name": "active session clone", 
    "description": "Cloned session from active one", 
    "activate": true, 
    "enable_tracking": true 
}
```

Response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "active session clone", 
    "description": "Cloned session from active one", 
    "slugname": "active-session-clone", 
    "is_active": true, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:30:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": null
}
```

> This example clones the previously created session.
> Here the name is present and therefore the slugname is set according to it.  
> The previous session becomes unactive and saves apps usage time

### Get apps usage data

Right away, the user wants to check how much time he has spent in applications through the 'brave-sky-dragon' session, that was created at first:

Request:

```http
GET /session/brave-sky-dragon/apps HTTP/1.1
Authorization: Bearer your-access-token
```

Successful Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[ 
    { 
        "name": "Google Chrome", 
        "exe": "C:\Program Files\Google\Chrome\Application\chrome.exe", 
        "cmdline": ""C:\Program Files\Google\Chrome\Application\chrome.exe"", 
        "is_active": true, 
        "usage_periods": [ 
            { 
                "started_at": "2024-04-26T10:00:00Z", 
                "ended_at": "2024-04-26T11:00:00Z" 
            } 
            ], 
        "total_seconds": 3600 
    } 
]
```

> This data contains "usage_periods" - time periods when the application was opened and active from "started_at" to "ended_at".
> "total_seconds" is the sum of all these periods, so it's the complete time of application usage

### Deactivate active session

Let's imagine that in this new session clone, the user didn't do anything productive and just watched YouTube videos. And he wants to deactivate this session and not to save application usage (so then it does not appear in the history). We can make it like so:

Request:

```http
POST /active-session/deactivate?save_usage=false HTTP/1.1
Authorization: Bearer your-access-token
```

Successful response:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{ 
    "name": "active session clone", 
    "description": "Cloned session from active one", 
    "slugname": "active-session-clone", 
    "is_active": false, 
    "is_tracking": true, 
    "created_at": "2024-04-26T12:30:00Z", 
    "saved_at": null, 
    "restored_at": null, 
    "last_active_at": null
}
```

And then lets check the apps usage for this session:

Request:

```http
GET /session/active-session-clone/apps HTTP/1.1
Authorization: Bearer your-access-token
```

Successful Response:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[ 
    { 
        "name": "Google Chrome", 
        "exe": "C:\Program Files\Google\Chrome\Application\chrome.exe", 
        "cmdline": ""C:\Program Files\Google\Chrome\Application\chrome.exe"", 
        "is_active": true, 
        "usage_periods": [] 
    } 
]
```

> In this example the usage data was not saved, so it's empty

## Future Improvements

- Linux and macOS support
- Docker containerization
- OAuth2 authentication (Google, GitHub)
- Full frontend client for CloudDesk
- More detailed application analytics

## License

This project is licensed under the Apache 2.0 License.
   
