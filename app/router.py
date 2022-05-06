from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Request, File, Depends, BackgroundTasks, status, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
from sqlalchemy.orm import Session

# my imports
from app.infra.sqlalchemy.config.database import SessionLocal
from app.controllers import get_nfe_controller
from app.provider.save_xml import save_xml
from random import randint


def get_db() -> Session:
    """Function responsible for capturing the environment variables

    Parameters:
    None

    Returns:
    Session: Returns a database session

   """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)) -> _TemplateResponse:
    """Function responsible for receiving a request in the "/" and returns an html template.

    Parameters:
    request (Request): Request class
    db (Session): database session

    Returns:
    _TemplateResponse: Returns an HTML template

   """

    # gets all related data from all NFe.
    data = get_nfe_controller.get_all_nfe(db)
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "data": data})


@router.get("/api/xml/{nfe_id}")
async def list_xml(nfe_id: str, db: Session = Depends(get_db)) -> dict:
    """Function responsible for receiving a request in the "/api/xml/{nfe_id}" and returns an html template.

    Parameters:
    nfe_id (str): id of one Nfe
    db (Session): database session

    Returns:
    dict: Returns a dictionary that will be parsed in json

   """

    # get all data related to an NFe
    result = get_nfe_controller.get_nfe(db, nfe_id)
    return result


@router.get("/files/", response_class=FileResponse)
async def file_example() -> str:
    """route that returns a valid XML example.

    Returns:
        returns a string that is parsed to a FIleResponse.
    """
    if randint(0, 1):
        return "test_1.xml"
    return "test_2.xml"


@router.post("/files/")
async def create_upload_files(background_tasks: BackgroundTasks, files: list[bytes] = File(...), db: Session = Depends(get_db)
                              ) -> RedirectResponse:
    """Function responsible for receiving a request in "/files/" and redirecting it to "/" after forwarding the data for processing.

    Parameters:
    background_tasks (BackgroundTasks): BackgroundTasks
    files (list[bytes]): list[bytes]
    db (Session): database session

    Returns:
    RedirectResponse: Redirect to root

   """
    # start a background task for data processing
    background_tasks.add_task(save_xml, files, db)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
