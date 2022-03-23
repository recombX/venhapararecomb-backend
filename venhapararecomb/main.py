from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .infra.database import engine
from .provider.save_xml import save_xml
from .infra.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "id": "id", "message": "None"})


@app.post("/uploadfiles/", response_class=HTMLResponse)
def create_upload_files(request: Request, files: list[UploadFile]):
    data = save_xml(files)
    result = dict(*data)

    return templates.TemplateResponse("home.html", {"request": request, "message": result})
