from .base import BaseRepository
from ..models import AppUsagePeriods, DeviceSessionApps, Application
from typing import Any


class AppsUsageRepository(BaseRepository):
    model = AppUsagePeriods

    def save_apps_usage(self, usage_data: dict[str, Any]):
        if usage_data is None:
            return

        for usage_item in usage_data.values():
            session_app = (
                self.db.query(DeviceSessionApps)
                .join(DeviceSessionApps.application)
                .filter(Application.exe == usage_item["exe"])
                .first()
            )

            for track in usage_item["tracking"]:
                start, end = track["start"], track["end"]

                usagePeriod = AppUsagePeriods(
                    session_app_id=session_app.id, started_at=start, ended_at=end
                )
                self.db.add(usagePeriod)

        self.db.commit()
