from ..utils.repositories import BaseRepository
from ..models import DeviceSession, DeviceSessionApps, Application
from typing import Any


class DeviceSessionrepository(BaseRepository):
    def get_by_slugname(self, slugname: str) -> DeviceSession | None:
        return (
            self.db.query(DeviceSession)
            .filter(DeviceSession.slugname == slugname)
            .first()
        )

    def get_all(self) -> list[DeviceSession]:
        return self.db.query(DeviceSession).all()

    def create(self, session_data: dict[str, Any], device_id: str) -> DeviceSession:
        session = DeviceSession(**session_data, device_id=device_id)
        self.db.add(session)
        self.db.commit()

        return session

    def delete(self, session):
        self.db.delete(session)
        self.db.commit()

    def clear_state(self, session: DeviceSession) -> DeviceSession:
        # deleting all states
        old_session_apps = (
            self.db.query(DeviceSessionApps)
            .filter(DeviceSessionApps.device_session_id == session.id)
            .all()
        )

        for app in old_session_apps:
            self.db.delete(app)

        self.db.commit()

        return session

    def update_state(
        self, session: DeviceSession, apps_data: dict[str, Any]
    ) -> DeviceSession:
        for app in apps_data:
            found_app = (
                self.db.query(Application)
                .filter(
                    Application.device_id == session.device.id,
                    Application.exe == app["exe"],
                )
                .first()
            )

            if found_app:
                app_state = DeviceSessionApps(
                    device_session_id=session.id, application_id=found_app.id
                )
                self.db.add(app_state)

        self.db.commit()

        return session
