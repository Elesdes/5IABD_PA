from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.user_services import request_admin, request_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="./templates/")


@router.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    if request_admin(request):
        return templates.TemplateResponse(
            name="users.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/models", response_class=HTMLResponse)
async def models(request: Request):
    if request_admin(request):
        return templates.TemplateResponse(
            name="models.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/mymodels", response_class=HTMLResponse)
async def mymodels(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(
            name="mymodels.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/mydevices", response_class=HTMLResponse)
async def mydevices(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(
            name="mydevices.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(
            name="profile.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/devices", response_class=HTMLResponse)
async def devices(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(
            name="devices.html", context={"request": request}
        )
    return templates.TemplateResponse(name="index.html", context={"request": request})
