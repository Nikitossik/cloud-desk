from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .session_tracker import SessionTracker
from ..models import Device, DeviceSession
from ..models.device_session_events import DeviceSessionEvent, SessionEventType
from ..repositories import DeviceSessionRepository, AppUsageRepository
from ..schemas.device_session import DeviceSessionIn, DeviceSessionUpdate, DeviceSessionWithReport, DeviceSessionOut, DeviceSessionTrashActionIn
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
        
    def get_all_sessions(self, device: Device, deleted_only: bool = False) -> list[DeviceSession]:
        if deleted_only:
            return [session for session in device.sessions if session.last_deleted_at is not None]
        return device.sessions
        
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
            self._add_session_event(new_session, SessionEventType.STARTED)

        return new_session

    def _add_session_event(self, session: DeviceSession, event_type: SessionEventType):
        session_event = DeviceSessionEvent(
            session_id=session.id,
            event_type=event_type,
        )
        self.device_session_repo.db.add(session_event)
        self.device_session_repo.db.commit()
    
    def update_session(self, session: DeviceSession, session_update: DeviceSessionUpdate, device: Device) -> DeviceSession:
        session_data = session_update.model_dump(exclude_unset=True)
        is_deleted_provided = "is_deleted" in session_data
        is_deleted = False
        was_deleted = session.last_deleted_at is not None
        
        if session_data.get("name"):
            session_data["name"], session_data["slugname"] = generate_name_and_slug(session_data.get("name"))
            found_session = self.device_session_repo.get_by_slugname(session_data["slugname"], device)
            
            if found_session and found_session.id != session.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Session with the given name already exists",
                )
        
        session_to_update = session

        if is_deleted_provided:
            is_deleted = session_data.pop("is_deleted")

            if is_deleted:
                session_to_update = self.stop_session(session)
                session_data["last_deleted_at"] = datetime.now()
            else:
                session_data["last_deleted_at"] = None
            
        updated_session = self.device_session_repo.update(session_to_update, session_data)

        if is_deleted_provided:
            if is_deleted and not was_deleted:
                self._add_session_event(updated_session, SessionEventType.MOVED_TO_TRASH)
            if (not is_deleted) and was_deleted:
                self._add_session_event(updated_session, SessionEventType.RESTORED_FROM_TRASH)

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
        self._add_session_event(started_session, SessionEventType.STARTED)

        return started_session

    def stop_last_active_session(self, device: Device):
        last_active_session = self.device_session_repo.get_active_session(device)

        if last_active_session:
            self.stop_session(last_active_session)

    def stop_session(
        self, session: DeviceSession
    ) -> DeviceSession:
        if not session.is_active:
            return session

        saved_session = self.save_session_state(session)

        saved_session = self.device_session_repo.update(
            saved_session,
            {"is_active": False, "last_active_at": datetime.now()},
        )

        SessionTracker.stop(saved_session.id)
        self._add_session_event(saved_session, SessionEventType.STOPPED)

        return saved_session

    def save_session_state(self, session: DeviceSession) -> DeviceSession:
        running_apps_data = uc.get_running_applications()

        updated_session = self.device_session_repo.update_apps_state(
            session, running_apps_data
        )

        return updated_session

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
            new_active_session, {"last_restored_at": datetime.now(tz=timezone.utc)}
        )
        self._add_session_event(new_active_session, SessionEventType.RESTORED)

        return DeviceSessionWithReport(
            **DeviceSessionOut.model_validate(new_active_session).model_dump(),
            report=restore_report
        )

    def delete_all_sessions(self, device: Device):
        for session in device.sessions:
            self.delete_session(session)

    def _select_deleted_sessions(self, device: Device, action_data: DeviceSessionTrashActionIn) -> list[DeviceSession]:
        if action_data.all:
            return [session for session in device.sessions if session.last_deleted_at is not None]

        selected_ids = set(action_data.session_ids or [])
        return [
            session
            for session in device.sessions
            if session.last_deleted_at is not None and session.id in selected_ids
        ]

    def purge_trash(self, device: Device, purge_data: DeviceSessionTrashActionIn):
        sessions_to_delete = self._select_deleted_sessions(device, purge_data)

        for session in sessions_to_delete:
            self.device_session_repo.delete_instance(session)

    def restore_trash(self, device: Device, restore_data: DeviceSessionTrashActionIn):
        sessions_to_restore = self._select_deleted_sessions(device, restore_data)

        for session in sessions_to_restore:
            restored_session = self.device_session_repo.update(session, {"last_deleted_at": None})
            self._add_session_event(restored_session, SessionEventType.RESTORED_FROM_TRASH)
