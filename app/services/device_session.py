from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .session_tracker import SessionTracker
from ..models import Device, DeviceSession
from ..repositories import DeviceSessionRepository, AppUsageRepository
from ..schemas import DeviceSessionIn, ApplicationBase
import app.utils.core as uc
from datetime import datetime, timezone
from typing import Any


class DeviceSessionService:
    def __init__(self, db: Session):
        self.device_session_repo: DeviceSessionRepository = DeviceSessionRepository(db)
        self.app_usage_repo: AppUsageRepository = AppUsageRepository(db)

    def create_session(
        self, device_session: DeviceSessionIn, device: Device
    ) -> DeviceSession:
        session_data = device_session.model_dump()

        session_data["device_id"] = device.id
        session_data["is_active"] = session_data["activate"]

        if session_data["is_active"]:
            self.deactivate_last_active_session(device)

        found_session = self.device_session_repo.get_by_slugname(
            session_data["slugname"], device
        )

        if found_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Session with the given name already exists",
            )

        new_session = self.device_session_repo.create(session_data)

        SessionTracker.start(new_session.id)

        return new_session

    def delete_session(self, session: DeviceSession):
        SessionTracker.stop(session.id)
        self.device_session_repo.delete_instance(session)

    def activate_session(self, session: DeviceSession, device: Device) -> DeviceSession:
        if session.is_active:
            return session

        self.deactivate_last_active_session(device)

        activated_session = self.device_session_repo.update(
            session, {"is_active": True}
        )

        SessionTracker.start(activated_session.id)

        return activated_session

    def deactivate_last_active_session(self, device: Device):
        last_active_session = self.device_session_repo.get_active_session(device)

        if last_active_session:
            self.deactivate_session(last_active_session)

    def deactivate_session(
        self, session: DeviceSession, save_usage: bool = True
    ) -> DeviceSession:
        saved_session = self.save_session_state(session)

        saved_session = self.device_session_repo.update(
            saved_session,
            {"is_active": False, "last_active_at": datetime.now()},
        )

        SessionTracker.stop(saved_session.id)

        return saved_session

    def save_session_state(self, session: DeviceSession) -> DeviceSession:
        running_apps_data = uc.get_running_applications()

        # datetime of saving
        saved_session = self.device_session_repo.update(
            session, {"saved_at": datetime.now(tz=timezone.utc)}
        )

        saved_session = self.device_session_repo.update_apps_state(
            saved_session, running_apps_data
        )

        return saved_session

    def save_session(self, session: DeviceSession) -> DeviceSession:
        saved_session = self.save_session_state(session)

        SessionTracker.start(saved_session.id)

        return saved_session

    def restore_session(self, session: DeviceSession, device: Device) -> DeviceSession:
        self.deactivate_last_active_session(device)
        
        apps_to_restore = [
            ApplicationBase.model_validate(app).model_dump() for app in session.apps
        ]

        uc.run_applications(apps_to_restore)
        new_active_session = self.activate_session(session, device)

        # datetime of restoring
        self.device_session_repo.update(
            new_active_session, {"restored_at": datetime.now(tz=timezone.utc)}
        )

        return new_active_session

    def delete_session_by_slugname(self, session_slug: str, device: Device):
        session = self.get_session_by_slugname(session_slug, device)

        self.delete_session(session)

    def clone_session_by_slugname(
        self, session_slug: str, device_session: DeviceSessionIn, device: Device
    ) -> DeviceSession:
        original_session = self.get_session_by_slugname(session_slug, device)
        session_clone = self.create_session(device_session, device)

        return self.device_session_repo.clone_state(original_session, session_clone)

    def get_active_session(self, device: Device) -> DeviceSession:
        session = self.device_session_repo.get_active_session(device)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active sessions at the moment",
            )

        return session

    def get_session_by_slugname(
        self, session_slug: str, device: Device
    ) -> DeviceSession:
        session = self.device_session_repo.get_by_slugname(session_slug, device)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session with the given name was not found",
            )

        return session

    def delete_all_sessions(self, device: Device):
        for session in device.sessions:
            self.delete_session(session)

    def activate_session_by_slug(
        self, session_slug: str, device: Device
    ) -> DeviceSession:
        session = self.get_session_by_slugname(session_slug, device)
        activated_session = self.activate_session(session, device)

        return activated_session

    def restore_session_by_slug(
        self, session_slug: str, device: Device
    ) -> DeviceSession:
        session_to_restore = self.get_session_by_slugname(session_slug, device)

        restored_session = self.restore_session(session_to_restore, device)
        return restored_session
