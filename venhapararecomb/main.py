from fastapi import FastAPI, Request, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from infra.database import engine, get_db
from provider.save_xml import save_xml

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": "None"})


@app.post("/uploadfiles/", response_class=HTMLResponse)
async def create_upload_files(request: Request, files: list[UploadFile], background_tasks: BackgroundTasks):
    background_tasks.add_task(save_xml, files)
    return templates.TemplateResponse("home.html", {"request": request, "message": "Processando os arquivos!"})
