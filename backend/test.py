from uuid import uuid4

from app.database import SessionLocal
from app.repositories import DeviceRepository, DeviceSessionRepository, ApplicationRepository
from app.models import SessionAppState


def add_fake_app_to_session(slugname: str) -> None:
    db = SessionLocal()
    try:
        device_repo = DeviceRepository(db)
        session_repo = DeviceSessionRepository(db)
        app_repo = ApplicationRepository(db)

        device = device_repo.get_local_device()
        if not device:
            print("[TEST] local device not found")
            return

        session = session_repo.get_by_slugname(slugname, device)
        if not session:
            print(f"[TEST] session not found by slugname={slugname}")
            return

        fake_name = f"fake_app_{uuid4().hex[:8]}"
        fake_path = rf"C:\__cloud_desk_test__\{fake_name}.exe"

        # Поддержка обоих вариантов поля: exe или exe_path
        app_payload = {
            "name": fake_name,
            "cmdline": fake_path,
            "device_id": device.id,
        }
        if hasattr(app_repo.model, "exe_path"):
            app_payload["exe_path"] = fake_path
        else:
            app_payload["exe"] = fake_path

        new_app = app_repo.create(app_payload)

        # Привязка приложения к сессии через state
        state = SessionAppState(
            session_id=session.id,
            application_id=new_app.id,
            is_active=True,
        )
        db.add(state)
        db.commit()

        print("[TEST] done")
        print(f"[TEST] session: {session.slugname} ({session.id})")
        print(f"[TEST] app: {new_app.name} ({new_app.id})")
        print(f"[TEST] state created: is_active={state.is_active}")

    except Exception as e:
        db.rollback()
        print(f"[TEST] error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_fake_app_to_session("1")