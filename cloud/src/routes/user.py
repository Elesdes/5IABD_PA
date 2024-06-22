from typing import Annotated
from markupsafe import escape
from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.user_services import (
    request_dashboard,
    request_login,
    request_register,
)
from src.services.cookie_services import set_response_cookie

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="./templates/")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(name="about.html", context={"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(
            name="mymodels.html", context={"request": request}
        )
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = templates.TemplateResponse(
        name="index.html", context={"request": request}
    )
    response.delete_cookie(key="ICARUS-Login")
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        name="register.html", context={"request": request}
    )


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    forename: Annotated[str, Form()],
) -> HTMLResponse:
    email = escape(email)
    password = escape(password)
    name = escape(name)
    forename = escape(forename)
    response = request_register(request, email, password, name, forename)
    if not response:
        posts = [
            {
                "bad_profile": '<div class="alert alert-warning" role="alert">Le profil existe déjà ou les informations données ne rentrent pas dans les critères</div>'
            }
        ]
        context = {"posts": posts, "request": request}
        return templates.TemplateResponse(name="register.html", context=context)
    return response


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]
) -> HTMLResponse:
    email = escape(email)
    password = escape(password)
    user = request_login(email, password)
    if user:
        return set_response_cookie(request, "mymodels.html", user.cookie)
    else:
        posts = [
            {
                "bad_profile": '<div class="alert alert-warning" role="alert">Mauvais identifiants</div>'
            }
        ]
        context = {"posts": posts, "request": request}
        return templates.TemplateResponse(name="login.html", context=context)
