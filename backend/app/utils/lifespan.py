from fastapi import FastAPI
from contextlib import asynccontextmanager
import traceback

from ..database import SessionLocal
from ..repositories import DeviceSessionRepository
from ..services import DeviceSessionService
from ..services.session_tracker import SessionTracker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # stopping last active session on shutdown if present and save usage data
    yield

    db = SessionLocal()
    session_id = SessionTracker.session_id

    try:
        print(f"[shutdown] session_id={session_id!r}")

        if session_id is not None:
            session = DeviceSessionRepository(db).get(session_id)
            print(f"[shutdown] session_found={bool(session)} active={getattr(session, 'is_active', None)}")

            if session and session.is_active:
                DeviceSessionService(db).stop_session(session)
                print("[shutdown] stop_session done")

    except Exception:
        print("[shutdown] error:")
        traceback.print_exc()
    finally:
        db.close()