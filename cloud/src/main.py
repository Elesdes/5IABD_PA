import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.cloud import storage
from src.routes import dashboard, user
from src.services import call_models, call_users, devices_services, download_upload
from src.utils.postgresql_utils import PostgreSQLUtils
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

"""
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
"""
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(download_upload.router)
app.include_router(user.router)
app.include_router(dashboard.router)
app.include_router(call_users.router)
app.include_router(call_models.router)
app.include_router(devices_services.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 500:
        return templates.TemplateResponse(
            "500.html", {"request": request}, status_code=500
        )
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "401.html",
            {"request": request, "status_code": exc.status_code, "detail": exc.detail},
            status_code=exc.status_code,
        )
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "status_code": exc.status_code, "detail": exc.detail},
            status_code=exc.status_code,
        )


@app.get("/test-error/500")
async def test_error_500():
    raise HTTPException(status_code=500, detail="Test d'erreur 500")


@app.get("/test-error/404")
async def test_error_404():
    raise HTTPException(status_code=404, detail="Test d'erreur 404")


@app.get("/test_db")
def test_db():
    db_utils = PostgreSQLUtils()
    users = []
    with db_utils as cursor:
        SQL_query = f"SELECT forename FROM USERS"
        cursor.execute(SQL_query)
        user_data = cursor.fetchall()
        for user in user_data:
            users.append({"forename": user[0]})
    return users


"""
@app.get("/test_blob", response_class=HTMLResponse, include_in_schema=False)
def test_blob(request: Request):
    client = storage.Client()
    bucket = client.get_bucket("icarus-gcp.appspot.com")
    blob = bucket.blob("test")
    blob.upload_from_filename("README.md")
    return templates.TemplateResponse(name="index.html", context={"request": request})
"""


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.ico")


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=3100)


if __name__ == "__main__":
    run()
