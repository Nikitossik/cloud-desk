import threading
import app.utils.core as core
from typing import Any

SESSION_TRACKERS: dict[str, Any] = {}


class SessionAppUsageTracker:
    @staticmethod
    def set(session_id: str):
        tracker = SessionAppUsageTracker.get(session_id)

        if not tracker:
            stop_event = threading.Event()
            usage_data = core.get_running_applications()

            SESSION_TRACKERS[session_id] = {
                "thread": threading.Thread(
                    target=core.track_apps_usage,
                    args=(stop_event, usage_data),
                    daemon=True,
                ),
                "stop_event": stop_event,
                "data": usage_data,
            }

        print(f"\nTracker set for session with id {session_id}")

    @staticmethod
    def get(session_id: str) -> dict[str, Any]:
        return SESSION_TRACKERS.get(session_id, None)

    @staticmethod
    def start(session_id: str):
        tracker = SessionAppUsageTracker.get(session_id)

        if not tracker:
            print(f"\nNo tracker for session {session_id}")
            return

        tracker["thread"].start()

        print(f"\nTracker started for session with id {session_id}")

    @staticmethod
    def stop(session_id: str, unset: bool = True) -> dict[str, Any] | None:
        tracker = SessionAppUsageTracker.get(session_id)

        if not tracker:
            print(f"\nNo tracker for session {session_id}")
            return None

        tracker["stop_event"].set()
        tracker["thread"].join()
        usage_data = core.update_apps_usage(tracker["data"])

        if unset:
            SessionAppUsageTracker.unset(session_id)

        return usage_data

    @staticmethod
    def unset(session_id: str):
        tracker = SessionAppUsageTracker.get(session_id)

        if tracker:
            SESSION_TRACKERS.pop(session_id)
            print(f"\nTracker unset for session {session_id}")

        print(f"\nNo tracker for session {session_id}")
