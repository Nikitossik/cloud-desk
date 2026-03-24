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
    
    def get_apps(
        self,
        session: DeviceSession,
        active_only: bool = False,
        include_launch_fields: bool = False,
    ):
        query = (
            self.db.query(SessionAppState, Application)
            .join(
                Application,
                SessionAppState.application_id == Application.id,
            )
            .filter(SessionAppState.session_id == session.id)
            .order_by(Application.name.asc())
        )

        if active_only:
            query = query.filter(SessionAppState.is_active.is_(True))

        rows = query.all()
        
        result_map = OrderedDict()

        for app_state, app in rows:
            if app.id not in result_map:
                app_data = {
                    "app_id": app.id,
                    "state_id": app_state.id,
                    "name": app.name,
                    "is_active": app_state.is_active,
                    "display_name": app.display_name,
                }

                if include_launch_fields:
                    app_data["exe"] = app.exe
                    app_data["cmdline"] = app.cmdline

                result_map[app.id] = app_data

        return list(result_map.values())

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
