from .base import BaseRepository
from ..models import AppUsagePeriod, SessionAppState, Application, DeviceSession
from typing import Any
from uuid import UUID

class AppUsageRepository(BaseRepository):
    model = AppUsagePeriod

    def get_apps_statistics(self, device_id: UUID | str):
        rows = (
            self.db.query(AppUsagePeriod, Application, DeviceSession)
            .join(Application, AppUsagePeriod.application_id == Application.id)
            .join(DeviceSession, AppUsagePeriod.session_id == DeviceSession.id)
            .filter(
                Application.device_id == device_id,
                AppUsagePeriod.ended_at.isnot(None),
            )
            .all()
        )

        app_map: dict[str, dict[str, Any]] = {}

        for usage_period, app, session in rows:
            duration = usage_period.duration
            if not duration:
                continue

            duration_seconds = int(duration.total_seconds())
            if duration_seconds <= 0:
                continue

            app_id = str(app.id)
            session_id = str(session.id)
            session_name = session.name

            if app_id not in app_map:
                app_map[app_id] = {
                    "app_id": app.id,
                    "display_name": app.display_name,
                    "usage": {},
                    "total_time": 0,
                }

            app_usage = app_map[app_id]["usage"]
            if session_id not in app_usage:
                app_usage[session_id] = {
                    "session_id": session.id,
                    "session_name": session_name,
                    "deleted_at": session.deleted_at,
                    "total_time": 0,
                }

            app_usage[session_id]["total_time"] += duration_seconds
            app_map[app_id]["total_time"] += duration_seconds

        result = []

        for app_data in app_map.values():
            usage_items = list(app_data["usage"].values())
            usage_items.sort(key=lambda item: item["total_time"], reverse=True)

            result.append(
                {
                    "app_id": app_data["app_id"],
                    "display_name": app_data["display_name"],
                    "total_time": app_data["total_time"],
                    "usage": usage_items,
                }
            )

        result.sort(
            key=lambda item: item["total_time"],
            reverse=True,
        )
        return result

    def get_sessions_statistics(self, device_id: UUID | str, all_sessions: bool = True):
        query = (
            self.db.query(AppUsagePeriod, Application, DeviceSession)
            .join(Application, AppUsagePeriod.application_id == Application.id)
            .join(DeviceSession, AppUsagePeriod.session_id == DeviceSession.id)
            .filter(
                DeviceSession.device_id == device_id,
                AppUsagePeriod.ended_at.isnot(None),
            )
        )

        if not all_sessions:
            query = query.filter(DeviceSession.deleted_at.is_(None))

        rows = query.all()

        session_map: dict[str, dict[str, Any]] = {}

        for usage_period, app, session in rows:
            duration = usage_period.duration
            if not duration:
                continue

            duration_seconds = int(duration.total_seconds())
            if duration_seconds <= 0:
                continue

            session_id = str(session.id)
            app_id = str(app.id)

            if session_id not in session_map:
                session_map[session_id] = {
                    "session_id": session.id,
                    "session_name": session.name,
                    "deleted_at": session.deleted_at,
                    "usage": {},
                }

            session_usage = session_map[session_id]["usage"]
            if app_id not in session_usage:
                session_usage[app_id] = {
                    "app_id": app.id,
                    "display_name": app.display_name,
                    "total_time": 0,
                }

            session_usage[app_id]["total_time"] += duration_seconds

        result = []

        for session_data in session_map.values():
            usage_items = list(session_data["usage"].values())
            usage_items.sort(key=lambda item: item["total_time"], reverse=True)

            result.append(
                {
                    "session_id": session_data["session_id"],
                    "session_name": session_data["session_name"],
                    "deleted_at": session_data["deleted_at"],
                    "usage": usage_items,
                }
            )

        result.sort(
            key=lambda item: sum(usage["total_time"] for usage in item["usage"]),
            reverse=True,
        )
        return result

    def save_apps_usage(self, usage_data: dict[str, Any], session_id: UUID | None = None):
        if usage_data is None:
            return

        for usage_item in usage_data.values():
            query = self.db.query(SessionAppState).join(SessionAppState.application)

            if session_id is not None:
                query = query.filter(
                    SessionAppState.session_id == session_id,
                    Application.exe == usage_item["exe"],
                )
            else:
                query = query.filter(Application.exe == usage_item["exe"])

            session_app = query.first()

            if not session_app:
                print(
                    f"[AppUsageRepository] no session_app for exe={usage_item['exe']} session_id={session_id}"
                )
                continue

            for track in usage_item["tracking"]:
                start, end = track["start"], track["end"]

                usagePeriod = AppUsagePeriod(
                    application_id=session_app.application_id,
                    session_id=session_app.session_id,
                    started_at=start,
                    ended_at=end,
                )
                self.db.add(usagePeriod)

        self.db.commit()
