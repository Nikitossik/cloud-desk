from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..database import SessionLocal
from ..repositories import DeviceRepository
from ..services import DeviceSessionService
from ..dependencies import get_current_device

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # deactivating last active session on shutdown if present and save usage data
    yield
    db = SessionLocal()
    try:
        device = DeviceRepository(db).get_local_device()
        if device:
            DeviceSessionService(db).deactivate_last_active_session(device)
    finally:
        db.close()