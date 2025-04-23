from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..tracking.app_usage import SessionAppUsageTracker
from ..models import Device, DeviceSession
from ..repositories import DeviceSessionrepository
from ..schemas import DeviceSessionIn, ApplicationBase
import app.utils.core as uc
from datetime import datetime, timezone
from typing import Any


class DeviceSessionService:
    def __init__(self, db: Session):
        self.device_session_repo: DeviceSessionrepository = DeviceSessionrepository(db)

    def create_session(
        self, device_session: DeviceSessionIn, device: Device
    ) -> DeviceSession:
        session_data = device_session.model_dump()

        session_data["device_id"] = device.id
        session_data["is_active"] = session_data["activate"]
        session_data["is_tracking"] = session_data["enable_tracking"]

        found_session = self.device_session_repo.get_by_slugname(
            session_data["slugname"], device
        )

        if found_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Session with the given name already exists",
            )

        new_session = self.device_session_repo.create(session_data)

        if new_session.is_active:
            self.deactivate_last_active_session(device)

        if new_session.is_tracking:
            self.start_session_tracking(new_session)

        return self.device_session_repo.create(session_data)

    def deactivate_last_active_session(self, device: Device):
        last_active_session = self.get_active_session(device)

        if last_active_session:
            self.deactivate_session(last_active_session)

    def start_session_tracking(self, session: DeviceSession):
        # running tracker

        SessionAppUsageTracker.set(session.id)
        SessionAppUsageTracker.start(session.id)

    def stop_session_tracking(self, session: DeviceSession):
        usage_data = SessionAppUsageTracker.stop(session.id)

        if usage_data:
            for _, app_data in usage_data.items():
                print(app_data["name"])

                for track in app_data["tracking"]:
                    print(
                        f"{datetime.strftime(track['start'], '%d/%m/%y %H:%M:%S')} - {datetime.strftime(track['end'], '%d/%m/%y %H:%M:%S')}"
                    )
                print("\n")

    def delete_session(self, session: DeviceSession):
        self.device_session_repo.delete_instance(session)

    def activate_session(self, session: DeviceSession, device: Device) -> DeviceSession:
        self.deactivate_last_active_session(device)

        activated_session = self.device_session_repo.update(
            session, {"is_active": True}
        )

        if session.is_tracking:
            self.start_session_tracking(activated_session)

        return activated_session

    def deactivate_session(self, session: DeviceSession) -> DeviceSession:
        self.stop_session_tracking(session)

        saved_session = self.save_session(session)

        self.device_session_repo.update(
            saved_session,
            {"is_active": False, "last_active_at": datetime.now()},
        )

        return saved_session

    def save_session(self, session: DeviceSession) -> DeviceSession:
        running_apps_data = uc.get_running_applications()

        # datetime of saving
        self.device_session_repo.update(
            session, {"saved_at": datetime.now(tz=timezone.utc)}
        )

        cleared_session = self.device_session_repo.clear_state(session)
        updated_session = self.device_session_repo.update_state(
            cleared_session, running_apps_data
        )

        if updated_session.is_tracking:
            self.stop_session_tracking(updated_session)
            self.start_session_tracking(updated_session)

        return updated_session

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
