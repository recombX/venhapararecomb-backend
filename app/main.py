from fastapi import FastAPI
from app.infra.settings import settings
from app.router import router
from app import __version__


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    redoc_url=None,
)

# records existing routes in the routes file
app.include_router(router)
