from .base import BaseRepository
from ..models import Device, DeviceSession, SessionAppState, Application, AppUsagePeriod
from typing import Any
import sqlalchemy as sa
from collections import OrderedDict

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
    
    def get_apps(self, session: DeviceSession):
        rows = (
        self.db.query(SessionAppState, Application)
            .join(
                Application,
                SessionAppState.application_id == Application.id,
            )
            .filter(SessionAppState.session_id == session.id)
            .order_by(Application.name.asc())
            .all()
        )
        
        result_map = OrderedDict()

        for app_state, app in rows:
            if app.id not in result_map:
                result_map[app.id] = {
                    "app_id": app.id,
                    "state_id": app_state.id,
                    "name": app.name,
                    "is_active": app_state.is_active,
                    "display_name": app.display_name,
                }

        return list(result_map.values())

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
