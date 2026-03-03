from .base import BaseRepository
from ..models import Device
from ..utils.core import get_mac_address

class DeviceRepository(BaseRepository):
    model = Device

    def get_by_user_id(self, user_id: int) -> list[Device]:
        return self.db.query(Device).filter(Device.user_id == user_id).all()

    def get_by_user_and_fingerprint(self, user_id: int, fingerprint: str) -> Device | None:
        return (
            self.db.query(Device)
            .filter(Device.user_id == user_id, Device.fingerprint == fingerprint)
            .first()
        )
        
    def get_local_device(self) -> Device | None:
        fingerprint = get_mac_address()
        return self.db.query(Device).filter(Device.fingerprint == fingerprint).first()
