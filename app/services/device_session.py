from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Device, DeviceSession
from ..repositories import DeviceSessionrepository, DeviceRepository
from ..schemas import DeviceSessionIn, ApplicationBase
from .device import DeviceService
import app.utils.core as uc


class DeviceSessionService:
    def __init__(self, db: Session):
        self.device_service: DeviceService = DeviceService(db)
        self.device_session_repo: DeviceSessionrepository = DeviceSessionrepository(db)
        self.device_repo: DeviceRepository = DeviceRepository(db)

    def create(self, session_model: DeviceSessionIn, device: Device) -> DeviceSession:
        # session is active by default

        session_data = session_model.model_dump()

        return self.device_session_repo.create(session_data, device.id)

    def get_by_slug(self, session_slug: str, device: Device) -> DeviceSession:
        session = self.device_session_repo.get_by_slugname(session_slug)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session with the given name was not found",
            )

        return session

    def delete(self, session_slug: str, device: Device):
        session = self.get_by_slug(session_slug, device)

        self.device_session_repo.delete(session)

    def activate_by_slug(self, session_slug: str, device: Device) -> DeviceSession:
        session = self.get_by_slug(session_slug, device)
        activated_session = self.device_repo.activate_session(session, device)
        return activated_session

    def save_state(self, device: Device) -> DeviceSession:
        running_apps_data = uc.get_running_applications()

        active_session = self.device_service.get_active_session(device)
        cleared_session = self.device_session_repo.clear_state(active_session)
        return self.device_session_repo.update_state(cleared_session, running_apps_data)

    def restore_state(self, session_slug: str, device: Device) -> DeviceSession:
        session_to_restore = self.get_by_slug(session_slug, device)
        apps_to_restore = [
            ApplicationBase.model_validate(app).model_dump()
            for app in session_to_restore.apps
        ]

        uc.run_applications(apps_to_restore)
        new_active_session = self.activate_by_slug(session_slug, device)

        return new_active_session
