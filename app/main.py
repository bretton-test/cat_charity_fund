from fastapi import FastAPI

from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.api.routers import main_router

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
