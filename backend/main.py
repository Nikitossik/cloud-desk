import uvicorn

from fastapi import FastAPI

from app.database import engine, Base
from app.models import (
    User,
    Device,
    Application,
    DeviceSession,
    SessionAppState,
    AppUsagePeriod,
)
import app.routes as r
from api_docs.app_docs import APP_DOCS
from app.config import setting
from app.utils.lifespan import lifespan

app = FastAPI(**APP_DOCS, lifespan=lifespan)

Base.metadata.create_all(bind=engine)
app.include_router(r.auth_route)
app.include_router(r.device_route)
app.include_router(r.active_session_route)
app.include_router(r.session_route)

if __name__ == "__main__":
    uvicorn.run("main:app", host=setting.HOST, port=8000, reload=True)
