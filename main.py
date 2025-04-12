import uvicorn

from app.routes import user_route, auth_route, test_route
from fastapi import FastAPI

from app.models import Base
from app.database import engine

# error handling
# jwt auth, what is OAuth2

# learn more about pydanctic, fastapi dependencies, code structure
# database migrations alembic


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(user_route)
app.include_router(auth_route)
app.include_router(test_route)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
