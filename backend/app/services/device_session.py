from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .session_tracker import SessionTracker
from ..models import Device, DeviceSession
from ..repositories import DeviceSessionRepository, AppUsageRepository
from ..schemas.device_session import DeviceSessionIn, DeviceSessionUpdate, DeviceSessionWithReport, DeviceSessionOut
from ..schemas.application import ApplicationRestoreReportOut
from ..utils.naming import generate_name_and_slug
import app.utils.core as uc
from datetime import datetime, timezone
import time
from typing import Any
from uuid import UUID

class DeviceSessionService:
    def __init__(self, db: Session):
        self.device_session_repo: DeviceSessionRepository = DeviceSessionRepository(db)
        self.app_usage_repo: AppUsageRepository = AppUsageRepository(db)
        
    def get_session_by_id(
        self, session_id: UUID, device: Device
    ) -> DeviceSession:
        session = self.device_session_repo.get(session_id)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session with the given ID was not found",
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
    
    def get_active_session(self, device: Device) -> DeviceSession:
        session = self.device_session_repo.get_active_session(device)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active sessions at the moment",
            )

        return session
    
    def get_apps(
        self,
        session: DeviceSession,
        active_only: bool = False,
        include_launch_fields: bool = False,
    ):
        return self.device_session_repo.get_apps(
            session,
            active_only=active_only,
            include_launch_fields=include_launch_fields,
        )

    def create_session(
        self, device_session: DeviceSessionIn, device: Device
    ) -> DeviceSession:
        session_data = device_session.model_dump(exclude_unset=True)

        session_data["device_id"] = device.id
        session_data["is_active"] = session_data.pop("start")

        if session_data["is_active"]:
            self.stop_last_active_session(device)
        
        session_data["name"], session_data["slugname"] = generate_name_and_slug(session_data.get("name"))

        found_session = self.device_session_repo.get_by_slugname(session_data["slugname"], device)
        if found_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Session with the given name already exists",
            )

        new_session = self.device_session_repo.create(session_data)

        if new_session.is_active:
            SessionTracker.start(new_session.id)

        return new_session
    
    def update_session(self, session: DeviceSession, session_update: DeviceSessionUpdate, device: Device) -> DeviceSession:
        session_data = session_update.model_dump(exclude_unset=True)
        
        if session_data.get("name"):
            session_data["name"], session_data["slugname"] = generate_name_and_slug(session_data.get("name"))
            found_session = self.device_session_repo.get_by_slugname(session_data["slugname"], device)
            
            if found_session and found_session.id != session.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Session with the given name already exists",
                )
            
        updated_session = self.device_session_repo.update(session, session_data)

        return updated_session

    def delete_session(self, session: DeviceSession):
        stopped_session = self.stop_session(session)
        self.device_session_repo.delete_instance(stopped_session)

    def start_session(self, session: DeviceSession, device: Device) -> DeviceSession:
        if session.is_active:
            return session

        self.stop_last_active_session(device)

        started_session = self.device_session_repo.update(
            session, {"is_active": True}
        )

        SessionTracker.start(started_session.id)

        return started_session

    def stop_last_active_session(self, device: Device):
        last_active_session = self.device_session_repo.get_active_session(device)

        if last_active_session:
            self.stop_session(last_active_session)

    def stop_session(
        self, session: DeviceSession
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

    def restore_session(self, session: DeviceSession, device: Device) -> DeviceSessionWithReport:
        self.stop_last_active_session(device)
        
        apps_to_restore = self.get_apps(
            session,
            active_only=True,
            include_launch_fields=True,
        )

        restore_report = [
            ApplicationRestoreReportOut.model_validate(item).model_dump()
            for item in uc.run_applications(apps_to_restore)
        ]
        new_active_session = self.start_session(session, device)
        
        time.sleep(1)
        running_apps_data = uc.get_running_applications()
        self.device_session_repo.update_apps_state(
            new_active_session, running_apps_data
        )

        # datetime of restoring
        self.device_session_repo.update(
            new_active_session, {"restored_at": datetime.now(tz=timezone.utc)}
        )

        return DeviceSessionWithReport(
            **DeviceSessionOut.model_validate(new_active_session).model_dump(),
            report=restore_report
        )

    def clone_session(
        self, original_session: DeviceSession, new_session: DeviceSessionIn, device: Device
    ) -> DeviceSession:
        session_clone = self.create_session(new_session, device)

        return self.device_session_repo.clone_state(original_session, session_clone)

    def delete_all_sessions(self, device: Device):
        for session in device.sessions:
            self.delete_session(session)
