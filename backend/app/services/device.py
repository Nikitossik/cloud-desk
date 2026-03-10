from ..repositories import DeviceRepository, ApplicationRepository
from sqlalchemy.orm import Session
import app.utils.core as uc
import app.utils.icons as ui
from pathlib import Path
from ..models import Device, Application
from ..schemas.device import DeviceUpdate
from typing import Any
from datetime import datetime
from fastapi import HTTPException, status

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
            device_data['last_seen_at'] = datetime.utcnow()
            new_device = self.device_repo.create(device_data)
            return new_device
        self.device_repo.update(device, {"last_seen_at": datetime.utcnow()})
        return device

    def bind_device_fingerprint(self, user_id: int, target_device_id: str, new_fingerprint: str) -> Device:
        target_device = self.device_repo.get(target_device_id)

        if not target_device or target_device.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        found_with_fingerprint = self.device_repo.get_by_user_and_fingerprint(user_id, new_fingerprint)

        if found_with_fingerprint and found_with_fingerprint.id != target_device.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Fingerprint is already bound to another device",
            )

        return self.device_repo.update(
            target_device,
            {
                "fingerprint": new_fingerprint,
                "last_seen_at": datetime.utcnow(),
            },
        )

    def create_device_with_fingerprint(
        self,
        user_id: int,
        new_fingerprint: str,
        display_name: str | None = None,
    ) -> Device:
        found_with_fingerprint = self.device_repo.get_by_user_and_fingerprint(user_id, new_fingerprint)

        if found_with_fingerprint:
            return self.device_repo.update(
                found_with_fingerprint,
                {"last_seen_at": datetime.utcnow()},
            )

        device_data = uc.get_device_data()
        device_data["user_id"] = user_id
        device_data["fingerprint"] = new_fingerprint
        device_data["display_name"] = display_name
        device_data["last_seen_at"] = datetime.utcnow()
        return self.device_repo.create(device_data)
    
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
                new_app = self.application_repo.create({**app, "device_id": device.id})
                icon_key = ui.save_application_icon(new_app.id, app.get("exe"))
                if icon_key:
                    self.application_repo.update(new_app, {"icon_key": icon_key})

        return device.apps

    def get_application_icon_path(self, app_id: str, device: Device) -> Path:
        app = self.application_repo.get_by_device_and_id(app_id, device.id)

        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        if not app.icon_key:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found")

        icon_path = ui.get_app_icon_abs_path(app.icon_key)
        if not icon_path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found")

        return icon_path
    
    def delete(self, device_id: str):
        device = self.device_repo.get(device_id)

        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        self.device_repo.delete_instance(device)

    def delete_device(self, device: Device):
        self.device_repo.delete_instance(device)
