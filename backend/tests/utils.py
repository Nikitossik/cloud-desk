def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "X-Device-Fingerprint": "test-device-fingerprint",
    }
