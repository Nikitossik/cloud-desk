import uvicorn

from fastapi import FastAPI

from app.database import engine, Base
from app.models import Device, Application, DeviceSession, DeviceSessionApps
import app.routes as r

app = FastAPI()

# попробовать получать сами объекты Window, найти способ как найти главное окно приложения
# клонирование сессий, добавление тегов
# livetracking с watchdog
# jwt auth
# пересмотреть pydantic-модели

# День 1–2: Авторизация

# День 3–4: Теги

# День 5: Клонирование

# День 6–7: MVP восстановления окон

# День 8: Прослушка (или описать идею)

# День 9: Тесты

# День 10: README + Docker + финальная шлифовка

Base.metadata.create_all(bind=engine)
app.include_router(r.device_route)
app.include_router(r.session_route)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
