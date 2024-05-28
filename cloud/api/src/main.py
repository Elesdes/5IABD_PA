from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from services import download_upload, call_users, call_models
from routes import user, dashboard
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(download_upload.router)
app.include_router(user.router)
app.include_router(dashboard.router)
app.include_router(call_users.router)
app.include_router(call_models.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="../templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 500:
        return templates.TemplateResponse(
            "500.html", {"request": request}, status_code=500
        )
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "status_code": exc.status_code, "detail": exc.detail},
            status_code=exc.status_code,
        )


@app.get("/test-error/500")
async def test_error():
    raise HTTPException(status_code=500, detail="Test d'erreur 500")


@app.get("/test-error/404")
async def test_error():
    raise HTTPException(status_code=404, detail="Test d'erreur 404")


def run():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run()
