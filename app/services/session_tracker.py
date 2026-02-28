import threading
import app.utils.core as core
from typing import Any
from ..database import SessionLocal
from ..repositories import DeviceSessionRepository, AppUsageRepository
from ..services.device import DeviceService
from datetime import datetime

class SessionTracker:
    lock = threading.RLock()
    thread: threading.Thread | None = None
    stop_event: threading.Event | None = None
    usage_data: dict[str, Any] = {}
    session_id: str | None = None

    @staticmethod
    def is_running() -> bool:
        return SessionTracker.thread is not None and SessionTracker.thread.is_alive()

    @staticmethod
    def sync_usage_data(current_apps: dict[str, Any]):
        now = datetime.now()
        usage_data = SessionTracker.usage_data

        opened_apps = {k: v for k, v in current_apps.items() if k not in usage_data}
        running_apps = {k: v for k, v in usage_data.items() if k in current_apps}
        closed_apps = {k: v for k, v in usage_data.items() if k not in current_apps}

        for app_key, app_data in opened_apps.items():
            app_data["tracking"].append({"start": now})
            usage_data[app_key] = app_data

        for _, app_data in running_apps.items():
            if len(app_data["tracking"]) == 0 or (
                "end" in app_data["tracking"][-1].keys()
            ):
                app_data["tracking"].append({"start": now})

        for app_key, app_data in closed_apps.items():
            if len(app_data["tracking"]) != 0:
                app_data["tracking"][-1].update({"end": now})

        if opened_apps or closed_apps:
            print(
                f"[SessionTracker] sync: opened={len(opened_apps)} closed={len(closed_apps)} running={len(running_apps)}"
            )
        
    @staticmethod        
    def end_apps_usage() -> dict[str, Any]:
        for _, app_data in SessionTracker.usage_data.items():
            now = datetime.now()
            for track in app_data["tracking"]:
                if "end" not in track.keys():
                    track["end"] = now

        return SessionTracker.usage_data

    @staticmethod
    def extract_closed_usage() -> dict[str, Any]:
        closed_usage = {}

        for app_key, app_data in SessionTracker.usage_data.items():
            closed_tracks = [
                track for track in app_data["tracking"] if "end" in track.keys()
            ]

            if closed_tracks:
                closed_usage[app_key] = {
                    "exe": app_data["exe"],
                    "name": app_data["name"],
                    "cmdline": app_data["cmdline"],
                    "tracking": closed_tracks,
                }

                app_data["tracking"] = [
                    track for track in app_data["tracking"] if "end" not in track.keys()
                ]

        return closed_usage

    @staticmethod
    def track_loop():
        print(f"[SessionTracker] loop started session_id={SessionTracker.session_id}")

        while SessionTracker.stop_event and not SessionTracker.stop_event.is_set():
            db = SessionLocal()

            try:
                session_repo = DeviceSessionRepository(db)
                usage_repo = AppUsageRepository(db)
                
                session = session_repo.get(SessionTracker.session_id)

                if not session or not session.is_active:
                    print(
                        f"[SessionTracker] session inactive or not found session_id={SessionTracker.session_id}, finalizing"
                    )

                    SessionTracker.end_apps_usage()
                    usage_to_save = SessionTracker.extract_closed_usage()

                    if usage_to_save:
                        usage_repo.save_apps_usage(usage_to_save, SessionTracker.session_id)
                        print(
                            f"[SessionTracker] final flush saved apps={len(usage_to_save)} session_id={SessionTracker.session_id}"
                        )

                    break

                current_apps = core.get_running_applications()

                device_service = DeviceService(db)
                device_service.sync_applications(session.device, current_apps)

                prev_exes = set(SessionTracker.usage_data.keys())
                current_exes = set(current_apps.keys())

                if prev_exes != current_exes:
                    session_repo.update_apps_state(session, current_apps)
                    print(
                        f"[SessionTracker] app states updated: prev={len(prev_exes)} current={len(current_exes)}"
                    )

                SessionTracker.sync_usage_data(current_apps)

                usage_to_save = SessionTracker.extract_closed_usage()
                if usage_to_save:
                    usage_repo.save_apps_usage(usage_to_save, SessionTracker.session_id)
                    print(
                        f"[SessionTracker] incremental flush saved apps={len(usage_to_save)} session_id={SessionTracker.session_id}"
                    )
            except Exception as e:
                print(f"[SessionTracker] loop error session_id={SessionTracker.session_id}: {e}")
            finally:
                db.close()

            SessionTracker.stop_event.wait(1)

        print(f"[SessionTracker] loop stopped session_id={SessionTracker.session_id}")

    @staticmethod
    def set(session_id: str):
        with SessionTracker.lock:
            SessionTracker.session_id = session_id
            SessionTracker.usage_data = core.get_running_applications()

            now = datetime.now()
            for app_data in SessionTracker.usage_data.values():
                app_data["tracking"].append({"start": now})

            print(
                f"[SessionTracker] state set session_id={session_id}, initial_apps={len(SessionTracker.usage_data)}"
            )


    @staticmethod
    def get(session_id: str) -> dict[str, Any] | None:
        if SessionTracker.session_id != session_id:
            return None

        if not SessionTracker.is_running():
            return None

        return {
            "thread": SessionTracker.thread,
            "stop_event": SessionTracker.stop_event,
            "data": SessionTracker.usage_data,
        }

    @staticmethod
    def start(session_id: str):
        with SessionTracker.lock:
            if SessionTracker.is_running() and SessionTracker.session_id == session_id:
                print(f"[SessionTracker] already running session_id={session_id}")
                return

            if SessionTracker.is_running() and SessionTracker.session_id != session_id:
                print(
                    f"[SessionTracker] switching tracker old_session={SessionTracker.session_id} new_session={session_id}"
                )
                SessionTracker.stop(SessionTracker.session_id)

            if SessionTracker.session_id != session_id:
                SessionTracker.set(session_id)

            SessionTracker.stop_event = threading.Event()
            SessionTracker.thread = threading.Thread(
                target=SessionTracker.track_loop,
                daemon=True,
            )
            SessionTracker.thread.start()
            print(f"[SessionTracker] thread started session_id={session_id}")

    @staticmethod
    def stop(session_id: str | None) -> dict[str, Any] | None:
        with SessionTracker.lock:
            if SessionTracker.session_id is None:
                print("[SessionTracker] stop ignored: no active tracker")
                return None

            if session_id is not None and SessionTracker.session_id != session_id:
                print(
                    f"[SessionTracker] stop ignored: requested={session_id}, active={SessionTracker.session_id}"
                )
                return None

            if SessionTracker.stop_event and SessionTracker.is_running():
                SessionTracker.stop_event.set()
                SessionTracker.thread.join()
                print(f"[SessionTracker] thread joined session_id={SessionTracker.session_id}")

            if SessionTracker.usage_data:
                db = SessionLocal()
                try:
                    usage_repo = AppUsageRepository(db)

                    SessionTracker.end_apps_usage()
                    usage_to_save = SessionTracker.extract_closed_usage()

                    if usage_to_save:
                        usage_repo.save_apps_usage(usage_to_save, SessionTracker.session_id)
                        print(
                            f"[SessionTracker] stop flush saved apps={len(usage_to_save)} session_id={SessionTracker.session_id}"
                        )
                except Exception:
                    print(f"[SessionTracker] stop flush failed session_id={SessionTracker.session_id}")
                finally:
                    db.close()

            SessionTracker.thread = None
            SessionTracker.stop_event = None
            SessionTracker.session_id = None
            SessionTracker.usage_data = {}
            print("[SessionTracker] state cleared")
            return None
