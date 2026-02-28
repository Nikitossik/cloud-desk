from .base import BaseRepository
from ..models import Device, DeviceSession, SessionAppState, Application
from typing import Any


class DeviceSessionRepository(BaseRepository):
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
        for session_app_state in original_session.session_app_states:
            cloned_app_state = SessionAppState(
                application_id=session_app_state.application_id,
                session_id=clone_session.id,
            )
            self.db.add(cloned_app_state)

        self.db.commit()
        self.db.refresh(clone_session)
        return clone_session

    def update_apps_state(
        self, session: DeviceSession, apps_data: dict[str, Any]
    ) -> DeviceSession:
        for session_app_state in session.session_app_states:
            session_app_state.is_active = False

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

            if not found_app:
                continue

            session_app_states = [
                session_app_state
                for session_app_state in session.session_app_states
                if session_app_state.application_id == found_app.id
            ]

            if len(session_app_states):
                session_app_state = session_app_states[0]
                session_app_state.is_active = True
            else:
                session_app_state = SessionAppState(
                    session_id=session.id, application_id=found_app.id
                )
                self.db.add(session_app_state)

        self.db.commit()

        return session
