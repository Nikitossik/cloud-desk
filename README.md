# CloudDesk

A system for managing user sessions, tracking application usage, and restoring working environments. Each session represents a list of open applications, and users can activate, restore, and monitor their sessions. Currently, the system is designed to work on Windows environments.

## Technologies

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite
- pywin32 + psutil (Windows process/window integration)

### Frontend

- React
- Vite
- TanStack Query
- Axios
- Tailwind CSS + shadcn/ui

### Platform

- Windows 10/11 (current supported OS)

## Features

- JWT-based user authentication
- Device registration and management
- Device resolution flow for users with multiple devices
- Session lifecycle management (create, start/stop, restore, delete)
- Background session tracker for app usage collection
- Real-time app status updates in active session via WebSocket
- User interface for managing sessions, devices, and app states
- Application usage analytics foundation


## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+
- Windows 10/11

### Installation and run (Backend + Frontend)

1. Clone the repository and go to project root:

```
git clone https://github.com/Nikitossik/cloud-desk.git
cd cloud-desk
```

2. Backend setup:

```
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```

3. Run backend API:

```
fastapi dev main.py
```

Backend URLs:

- API base: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

4. Frontend setup (new terminal):

```
cd frontend
npm install
```

5. Run frontend:

```
npm run dev
```

Frontend URL:

- App: `http://127.0.0.1:5173`

Detailed backend endpoint examples are available in [backend/docs](./backend/docs).

## Future Improvements

- Linux and macOS support
- Desktop application (Electron)
- Trash bin for deleted sessions with restore/cleanup flows
- More detailed application usage analytics across devices and sessions

## License

This project is licensed under the Apache 2.0 License.
   
