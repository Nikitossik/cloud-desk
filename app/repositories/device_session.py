from ..utils.repositories import BaseRepository
from ..models import Device, DeviceSession, DeviceSessionApps, Application
from typing import Any

from datetime import datetime


class DeviceSessionrepository(BaseRepository):
    model = DeviceSession

    def get_by_slugname(self, slugname: str, device: Device) -> DeviceSession | None:
        for session in device.sessions:
            if session.slugname == slugname:
                return session

        return None

    def get_active_session(self, device: Device) -> DeviceSession | None:
        for session in device.sessions:
            if session.is_active:
                return session

        return None

    def clone_state(
        self, original_session: DeviceSession, clone_session: DeviceSession
    ) -> DeviceSession:
        for app_state in original_session.app_states:
            cloned_app_state = DeviceSessionApps(
                application_id=app_state.application_id,
                device_session_id=clone_session.id,
            )
            self.db.add(cloned_app_state)

        self.db.commit()
        self.db.refresh(clone_session)
        return clone_session

    def update_apps_state(
        self, session: DeviceSession, apps_data: dict[str, Any]
    ) -> DeviceSession:
        for app_state in session.app_states:
            app_state.is_active = False

        self.db.commit()

        for app in apps_data.values():
            found_app = (
                self.db.query(Application)
                .filter(
                    Application.device_id == session.device.id,
                    Application.exe == app["exe"],
                )
                .first()
            )

            app_states = [
                app_state
                for app_state in session.app_states
                if app_state.application_id == found_app.id
            ]

            if len(app_states):
                app_state = app_states[0]
                app_state.is_active = True
            else:
                app_state = DeviceSessionApps(
                    device_session_id=session.id, application_id=found_app.id
                )
                self.db.add(app_state)

        self.db.commit()

        return session
