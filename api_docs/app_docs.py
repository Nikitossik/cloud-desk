APP_DOCS = {
    "title": "Cloud Desk API",
    "description": (
        "CloudDesk API allows users to manage application sessions, "
        "track active time across applications, and quickly restore working environments. "
        "Currently, a working environment represents a list of open applications within a session. "
        "The API provides functionality to create, activate, deactivate, and clone sessions, "
        "as well as monitor user activity and time spent within each session. "
        "Access to user devices and sessions is protected and requires authentication via user registration and login."
    ),
    "summary": "Manage sessions, track active application time, and restore your workspace effortlessly.",
    "version": "0.0.1",
    "contact": {
        "name": "Mykyta Rakhmanyi",
        "email": "nikita.rahmany@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "openapi_tags": [
        {
            "name": "auth",
            "description": (
                "Authentication endpoints for user registration, login, "
                "access token refresh, and retrieving current user information. "
                "All sensitive operations require valid authentication tokens."
            ),
        },
        {
            "name": "device",
            "description": (
                "Device endpoints for retrieving device information, deleting a registered device, "
                "and synchronizing installed applications. "
                "All operations require valid authentication tokens."
            ),
        },
        {
            "name": "active session",
            "description": (
                "Endpoints for managing the currently active device session, "
                "including retrieving session details, saving session state, "
                "enabling or disabling tracking of application usage, "
                "deactivating and restoring sessions, and cloning active sessions. "
                "If the active session is not found, the operation cannot be performed and the API returns a 404 error"
                "All operations require valid authentication tokens."
            ),
        },
        {
            "name": "session",
            "description": (
                "Endpoints for managing saved device sessions: creating, cloning, activating, restoring, "
                "retrieving session details, listing applications, and deleting sessions. "
                "If the session is not found, the operation cannot be performed and the API returns a 404 error."
                "All operations require valid authentication tokens."
            ),
        },
    ],
}
