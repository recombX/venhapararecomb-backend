from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, UploadFile, BackgroundTasks, Depends
from fastapi.templating import Jinja2Templates

from app.infra.sqlalchemy.config.database import SessionLocal
from app.provider.save_xml import save_xml
from app.controllers import get_nfe_controller
router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    data = get_nfe_controller.get_all_nfe(db)
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "data": data})


@router.get("/xml/{nfe_id}")
async def list_xml(nfe_id: str, db: Session = Depends(get_db)):
    result = get_nfe_controller.get_nfe(db, nfe_id)
    return result


@router.post("/uploadfiles/", response_class=HTMLResponse)
async def create_upload_files(request: Request, files: list[UploadFile], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(save_xml, files, db)
    return templates.TemplateResponse("home.html", {"request": request, "message": "result"})
