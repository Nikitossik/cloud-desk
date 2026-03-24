APP_DOCS = {
    "title": "CloudDesk API",
    "description": (
        "CloudDesk API allows users to manage device sessions, "
        "track active applications, and restore working environments. "
        "A working environment is represented by a session with application states. "
        "The API supports creating, starting, stopping, restoring, and deleting sessions, "
        "device-aware session flows, and authenticated user/device operations."
    ),
    "summary": "Manage sessions, track app activity, and restore workspace state.",
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
                "Authentication endpoints for registration, login, token refresh, "
                "and obtaining the current authenticated user."
            ),
        },
        {
            "name": "user",
            "description": (
                "User management endpoints for authenticated account-level operations, "
                "including retrieving and updating user profile data."
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
            "name": "session",
            "description": (
                "Endpoints for managing saved device sessions: creating, starting, stopping, restoring, "
                "retrieving session details, listing applications, and deleting sessions. "
                "If a session is not found, the API returns 404. "
                "All operations require valid authentication tokens."
            ),
        },
        {
            "name": "statistics",
            "description": (
                "Endpoints for aggregated application/session usage statistics "
                "for the current authenticated device."
            ),
        },
    ],
}