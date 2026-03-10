import asyncio
from collections import OrderedDict
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketException
from sqlalchemy.orm import Session

import app.dependencies as d
import app.models as md
import app.utils.core as uc
from app.services import DeviceService, DeviceSessionService

ws_session_route = APIRouter(prefix="/ws/session", tags=["session"])


def _build_signature_map(apps: list[dict]) -> OrderedDict[str, tuple]:
    signature_map: OrderedDict[str, tuple] = OrderedDict()

    for app in apps:
        app_id = app.get("app_id")
        if not app_id:
            continue

        app_key = str(app_id)
        signature_map[app_key] = (
            str(app.get("state_id")) if app.get("state_id") is not None else None,
            app.get("name"),
            bool(app.get("is_active")),
        )

    return signature_map


@ws_session_route.websocket("/active/apps")
async def ws_active_session_apps(
    websocket: WebSocket,
    db: Annotated[Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device_ws)],
):
    await websocket.accept()

    previous_signature_map: OrderedDict[str, tuple] = OrderedDict()

    try:
        while True:
            try:
                device_service = DeviceService(db)
                session_service = DeviceSessionService(db)
                active_session = session_service.get_active_session(device)

                current_apps_data = uc.get_running_applications()
                device_service.sync_applications(device, current_apps_data)
                session_service.device_session_repo.update_apps_state(active_session, current_apps_data)

                current_apps = session_service.get_apps(active_session)
                for app in current_apps:
                    app["app_id"] = str(app.get("app_id")) if app.get("app_id") is not None else None
                    app["state_id"] = str(app.get("state_id")) if app.get("state_id") is not None else None

                current_signature_map = _build_signature_map(current_apps)

                if not previous_signature_map:
                    await websocket.send_json(
                        {
                            "type": "snapshot",
                            "apps": current_apps,
                        }
                    )
                else:
                    upsert_apps = []

                    for app in current_apps:
                        app_key = str(app.get("app_id"))
                        if previous_signature_map.get(app_key) != current_signature_map.get(app_key):
                            upsert_apps.append(app)

                    if upsert_apps:
                        await websocket.send_json(
                            {
                                "type": "upsert",
                                "apps": upsert_apps,
                            }
                        )

                previous_signature_map = current_signature_map
            except WebSocketException as ws_exc:
                await websocket.close(code=ws_exc.code, reason=ws_exc.reason)
                return

            await asyncio.sleep(1)
    except Exception:
        await websocket.close()
