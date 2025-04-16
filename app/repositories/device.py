from ..utils.repositories import BaseRepository
from ..models import Device, Application, DeviceSession
from typing import Any


class DeviceRepository(BaseRepository):
    def get_by_mac_address(self, mac_address: str) -> Device | None:
        return self.db.query(Device).filter(Device.mac_address == mac_address).first()

    def create(self, device_data: dict) -> Device:
        device = Device(**device_data)
        self.db.add(device)
        self.db.commit()
        return device

    def delete(self, device: Device):
        self.db.delete(device)
        self.db.commit()

    def activate_session(
        self, device_session: DeviceSession, device: Device
    ) -> DeviceSession:
        self.deactivate_sessions(device)
        device_session.is_active = True
        self.db.commit()
        self.db.refresh(device_session)

        return device_session

    def get_active_session(self, device: Device) -> DeviceSession | None:
        for session in device.sessions:
            if session.is_active:
                return session

        return None

    def deactivate_sessions(self, device: Device):
        for session in device.sessions:
            session.is_active = False
            self.db.commit()
            self.db.refresh(session)

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
