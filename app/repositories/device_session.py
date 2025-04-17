from ..utils.repositories import BaseRepository
from ..models import Device, DeviceSession, DeviceSessionApps, Application
from typing import Any


class DeviceSessionrepository(BaseRepository):
    model = DeviceSession

    def get_by_slugname(self, slugname: str, device: Device) -> DeviceSession | None:
        for session in device.sessions:
            if session.slugname == slugname:
                return session

        return None

    def activate(self, device_session: DeviceSession, device: Device) -> DeviceSession:
        self.deactivate_all(device)
        device_session.is_active = True
        self.db.commit()
        self.db.refresh(device_session)

        return device_session

    def get_active_session(self, device: Device) -> DeviceSession | None:
        for session in device.sessions:
            if session.is_active:
                return session

        return None

    def deactivate_all(self, device: Device):
        for session in device.sessions:
            session.is_active = False

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
