from fastapi import FastAPI, Request, UploadFile, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .provider.save_xml import save_xml
from app.infra.sqlalchemy.config.database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static",
          StaticFiles(directory="app/static"), name="static")
app.mount("/public",
          StaticFiles(directory="app/public"), name="public")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": "None"})


@app.get("/xml", response_class=HTMLResponse)
async def list_xml(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": "data"})


@app.post("/uploadfiles/", response_class=HTMLResponse)
async def create_upload_files(request: Request, files: list[UploadFile], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(save_xml, files, db)
    return templates.TemplateResponse("home.html", {"request": request, "message": "result"})
