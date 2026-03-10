from .base import BaseRepository
from ..models import Application
from uuid import UUID
class ApplicationRepository(BaseRepository):
    model = Application

    def get_by_device_and_exe(self, exe: str, device_id: UUID) -> Application | None:
        return (
            self.db.query(Application)
            .filter(Application.exe == exe, Application.device_id == device_id)
            .first()
        )

    def get_by_device_and_id(self, app_id: UUID, device_id: UUID) -> Application | None:
        return (
            self.db.query(Application)
            .filter(Application.id == app_id, Application.device_id == device_id)
            .first()
        )
