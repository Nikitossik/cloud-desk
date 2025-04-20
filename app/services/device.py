from ..repositories.device import DeviceRepository
from sqlalchemy.orm import Session
import app.utils.core as uc
from ..models import Device, DeviceSession
from fastapi import HTTPException, status


class DeviceService:
    def __init__(self, db: Session):
        self.device_repo: DeviceRepository = DeviceRepository(db)

    def create_or_get_device(self, user_id: int) -> Device:
        mac_address = uc.get_mac_address()
        device = self.device_repo.get_by_user_and_mac(user_id, mac_address)

        if not device:
            device_data = uc.get_device_data()
            device_data["user_id"] = user_id
            new_device = self.device_repo.create(device_data)
            return new_device

        return device

    def sync_applications(self, device: Device):
        running_apps_data = uc.get_running_applications()

        return self.device_repo.update_applications(running_apps_data, device)

    def delete_device(self, device: Device):
        self.device_repo.delete_instance(device)
