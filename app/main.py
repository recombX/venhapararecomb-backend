from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI()

app.mount("/static",
          StaticFiles(directory="app/static"), name="static")
app.mount("/public",
          StaticFiles(directory="app/public"), name="public")

app.include_router(router)
