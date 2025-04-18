from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Device, DeviceSession
from ..repositories import DeviceSessionrepository
from ..schemas import DeviceSessionIn, ApplicationBase
import app.utils.core as uc
from datetime import datetime, timezone


class DeviceSessionService:
    def __init__(self, db: Session):
        self.device_session_repo: DeviceSessionrepository = DeviceSessionrepository(db)

    def create_session(
        self, device_session: DeviceSessionIn, device: Device, activate: bool = True
    ) -> DeviceSession:
        session_data = device_session.model_dump()
        session_data["device_id"] = device.id
        session_data["is_active"] = activate

        found_session = self.device_session_repo.get_by_slugname(
            session_data["slugname"], device
        )

        if found_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Session with the given name already exists",
            )

        if activate:
            self.deactivate_all(device)

        return self.device_session_repo.create(session_data)

    def clone_session_with_slugname(
        self,
        session_slug: str,
        device_session: DeviceSessionIn,
        device: Device,
        activate: bool = True,
    ) -> DeviceSession:
        original_session = self.get_session_by_slugname(session_slug, device)
        session_clone = self.create_session(device_session, device, activate)

        return self.device_session_repo.clone_state(original_session, session_clone)

    def get_active_session(self, device: Device) -> DeviceSession:
        session = self.device_session_repo.get_active_session(device)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active sessions at the moment",
            )

        return session

    def deactivate_all(self, device: Device):
        return self.device_session_repo.deactivate_all(device)

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

    def delete_session(self, session_slug: str, device: Device):
        session = self.get_session_by_slugname(session_slug, device)

        self.device_session_repo.delete_instance(session)

    def delete_all_sessions(self, device: Device):
        for session in device.sessions:
            self.device_session_repo.delete_instance(session)

    def activate_session_by_slug(
        self, session_slug: str, device: Device
    ) -> DeviceSession:
        last_active_session = self.get_active_session(device)

        # save the last datetime when the prev session was active
        self.device_session_repo.update(
            last_active_session, {"last_active_at": datetime.now(tz=timezone.utc)}
        )

        session = self.get_session_by_slugname(session_slug, device)
        activated_session = self.device_session_repo.activate(session, device)

        return activated_session

    def save_active_state(self, device: Device) -> DeviceSession:
        running_apps_data = uc.get_running_applications()

        active_session = self.get_active_session(device)

        # datetime of saving
        self.device_session_repo.update(
            active_session, {"saved_at": datetime.now(tz=timezone.utc)}
        )
        cleared_session = self.device_session_repo.clear_state(active_session)

        return self.device_session_repo.update_state(cleared_session, running_apps_data)

    def restore_session_by_slug(
        self, session_slug: str, device: Device
    ) -> DeviceSession:
        session_to_restore = self.get_session_by_slugname(session_slug, device)
        apps_to_restore = [
            ApplicationBase.model_validate(app).model_dump()
            for app in session_to_restore.apps
        ]

        uc.run_applications(apps_to_restore)
        new_active_session = self.activate_session_by_slug(session_slug, device)

        # datetime of restoring
        self.device_session_repo.update(
            new_active_session, {"restored_at": datetime.now(tz=timezone.utc)}
        )

        return new_active_session
