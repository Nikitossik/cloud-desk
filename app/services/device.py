from ..repositories.device import DeviceRepository
from sqlalchemy.orm import Session
import app.utils.core as uc
from ..models import Device, DeviceSession
from fastapi import HTTPException, status


class DeviceService:
    def __init__(self, db: Session):
        self.device_repo: DeviceRepository = DeviceRepository(db)

    def create_or_get_device(self):
        mac_address = uc.get_mac_address()
        device = self.device_repo.get_by_mac_address(mac_address)

        if not device:
            device_data = uc.get_device_data()
            new_device = self.device_repo.create(device_data)
            return new_device

        return device

    def get_active_session(self, device: Device) -> DeviceSession:
        session = self.device_repo.get_active_session(device)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active sessions at the moment",
            )

        return session

    def deactivate_sessions(self, device: Device):
        return self.device_repo.deactivate_sessions(device)

    def sync_applications(self, device: Device):
        running_apps_data = uc.get_running_applications()

        return self.device_repo.update_applications(running_apps_data, device)
