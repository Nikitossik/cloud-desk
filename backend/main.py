import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
from docs.app_docs import APP_DOCS
from app.config import setting, BASE_DIR
from app.utils.lifespan import lifespan

app = FastAPI(**APP_DOCS, lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


Base.metadata.create_all(bind=engine)
app.include_router(r.auth_route)
app.include_router(r.user_route)
app.include_router(r.device_route)
app.include_router(r.session_route)
app.include_router(r.ws_session_route)
app.include_router(r.statistics_route)

if __name__ == "__main__":
    uvicorn.run("main:app", host=setting.HOST, port=8000, reload=True)
