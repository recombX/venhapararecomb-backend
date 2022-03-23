from typing import List
from fastapi import FastAPI, Request, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from provider.save_xml import save_xml
from infra.database import database, models
from schemas.schemas import PersonView

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": "None"})


@app.get("/xml", response_model=List[PersonView])
async def list_xml():
    query = models['person'].select()
    return await database.fetch_all(query)
    # return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": data})


@app.post("/uploadfiles/", response_class=HTMLResponse)
async def create_upload_files(request: Request, files: list[UploadFile], background_tasks: BackgroundTasks):
    background_tasks.add_task(save_xml, files)
    return templates.TemplateResponse("home.html", {"request": request, "message": "result"})
