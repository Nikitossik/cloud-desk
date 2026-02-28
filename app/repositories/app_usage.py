from .base import BaseRepository
from ..models import AppUsagePeriod, SessionAppState, Application
from typing import Any


class AppUsageRepository(BaseRepository):
    model = AppUsagePeriod

    def save_apps_usage(self, usage_data: dict[str, Any], session_id: str | None = None):
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
