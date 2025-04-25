from ..utils.repositories import BaseRepository
from ..models import Device, Application
from typing import Any


class DeviceRepository(BaseRepository):
    model = Device

    def get_by_user_and_mac(self, user_id: int, mac_address: str) -> Device | None:
        return (
            self.db.query(Device)
            .filter(Device.user_id == user_id, Device.mac_address == mac_address)
            .first()
        )
