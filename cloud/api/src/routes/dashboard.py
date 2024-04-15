from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

@router.get("/mymodels", response_class=HTMLResponse)
async def mymodels(request: Request):
    return templates.TemplateResponse(
        name="mymodels.html", context={"request": request}
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplateResponse(
        name="profile.html", context={"request": request}
    )
