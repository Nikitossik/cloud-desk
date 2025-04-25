from ..utils.repositories import BaseRepository
from ..models import Device, Application
from typing import Any


class Applicationrepository(BaseRepository):
    model = Application

    def get_by_device_and_exe(self, exe: str, device_id) -> Application | None:
        return (
            self.db.query(Application)
            .filter(Application.exe == exe, Application.device_id == device_id)
            .first()
        )
