from ..repositories import DeviceRepository, ApplicationRepository
from sqlalchemy.orm import Session
import app.utils.core as uc
from ..models import Device, Application
from ..schemas.device import DeviceUpdate
from typing import Any
import uuid
from datetime import datetime

class DeviceService:
    def __init__(self, db: Session):
        self.device_repo: DeviceRepository = DeviceRepository(db)
        self.application_repo: ApplicationRepository = ApplicationRepository(db)
        
    def create_or_get_device(self, user_id: int, device_fingerprint: str) -> Device:
        device = self.device_repo.get_by_user_and_fingerprint(user_id, device_fingerprint)

        if not device:
            device_data = uc.get_device_data()
            device_data["user_id"] = user_id
            device_data['fingerprint'] = device_fingerprint
            new_device = self.device_repo.create(device_data)
            return new_device
        
        return device
    
    def update_current_device(self, device: Device, device_update: DeviceUpdate) -> Device:
        update_data = device_update.model_dump(exclude_unset=True)
        updated_device = self.device_repo.update(device, update_data)
        return updated_device

    def sync_applications(
        self, device: Device, apps_data: dict[str, Any] | None = None
    ) -> list[Application]:
        apps = apps_data if apps_data is not None else uc.get_running_applications()

        for app in apps.values():
            found_app = self.application_repo.get_by_device_and_exe(
                app["exe"], device.id
            )

            if not found_app:
                self.application_repo.create({**app, "device_id": device.id})

        return device.apps

    def delete_device(self, device: Device):
        self.device_repo.delete_instance(device)
