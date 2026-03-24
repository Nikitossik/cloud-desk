from fastapi import APIRouter, Depends
import sqlalchemy.orm as so

import app.models as md
import app.dependencies as d
from pathlib import Path
from typing import Annotated

from ..repositories import AppUsageRepository
from ..schemas.statistics import StatisticsAppOut, StatisticsSessionOut


statistics_route = APIRouter(prefix="/statistics", tags=["statistics"])
DOCS_PATH = Path(__file__).parent.parent.parent / "docs" / "statistics"


@statistics_route.get(
    "/apps",
    description=(DOCS_PATH / "get_statistics_apps.md").read_text(),
    summary="Returns per-application usage totals grouped by session.",
    response_model=list[StatisticsAppOut],
)
def get_apps_statistics(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
):
    return AppUsageRepository(db).get_apps_statistics(device.id)


@statistics_route.get(
    "/sessions",
    description=(DOCS_PATH / "get_statistics_sessions.md").read_text(),
    summary="Returns per-session usage totals grouped by application.",
    response_model=list[StatisticsSessionOut],
)
def get_sessions_statistics(
    *,
    db: Annotated[so.Session, Depends(d.get_db)],
    device: Annotated[md.Device, Depends(d.get_current_device)],
    all_sessions: bool = True,
):
    return AppUsageRepository(db).get_sessions_statistics(device.id, all_sessions=all_sessions)
