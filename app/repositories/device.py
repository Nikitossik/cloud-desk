from .base import BaseRepository
from ..models import Device
from ..utils.core import get_mac_address

class DeviceRepository(BaseRepository):
    model = Device

    def get_by_user_and_mac(self, user_id: int, mac_address: str) -> Device | None:
        return (
            self.db.query(Device)
            .filter(Device.user_id == user_id, Device.mac_address == mac_address)
            .first()
        )
        
    def get_local_device(self) -> Device | None:
        mac_address = get_mac_address()
        return self.db.query(Device).filter(Device.mac_address == mac_address).first()
