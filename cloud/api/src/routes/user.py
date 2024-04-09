from typing import Annotated

from fastapi import (
    Request,
    HTTPException,
    APIRouter,
    status,
    Form
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.user_services import request_dashboard, request_login, request_register
from services.cookie_services import set_response_cookie


router = APIRouter(
    prefix="/pages",
    tags=["pages"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="../templates/")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(name="about.html", context={"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request_dashboard(request):
        return templates.TemplateResponse(name="dashboard.html", context={"request": request})
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = templates.TemplateResponse(name="index.html", context={"request": request})
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
    forename: Annotated[str, Form()]
) -> HTMLResponse:
    response = request_register(request, email, password, name, forename)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User already exists or wrong profile."
        )
    return response


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]) -> HTMLResponse:
    user = request_login(email, password)
    if user:
        return set_response_cookie(request, "dashboard.html", user.cookie)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
