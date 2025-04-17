from ..utils.repositories import BaseRepository
from ..models import Device, Application
from typing import Any


class DeviceRepository(BaseRepository):
    model = Device

    def get_by_mac_address(self, mac_address: str) -> Device | None:
        return self.db.query(Device).filter(Device.mac_address == mac_address).first()

    def delete_instance(self, device: Device):
        self.db.delete(device)
        self.db.commit()

    def update_applications(
        self, apps: list[dict[str, Any]], device: Device
    ) -> list[Application]:
        for app in apps:
            found_app = (
                self.db.query(Application)
                .filter(
                    Application.device_id == device.id,
                    Application.exe == app["exe"],
                )
                .first()
            )

            if not found_app:
                new_app = Application(**app, device_id=device.id)
                self.db.add(new_app)
                self.db.commit()

        return device.apps
