from fastapi import (
    APIRouter,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")
router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="../templates/")


@router.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse(
        name="users.html", context={"request": request}
    )


@router.get("/models", response_class=HTMLResponse)
async def models(request: Request):
    return templates.TemplateResponse(
        name="models.html", context={"request": request}
    )

