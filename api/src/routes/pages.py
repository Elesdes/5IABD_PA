from fastapi import FastAPI, Request, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pages",
    tags=["pages"],
    responses={404: {"description": "Not found"}},)
templates = Jinja2Templates(directory="../templates/")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        name="about.html", context={"request": request}
    )
