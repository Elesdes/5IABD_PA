from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, HTMLResponse
import uvicorn
from starlette.templating import Jinja2Templates

from config.app_config import CONFIG
from services import download_upload
# Ne pas utiliser de chemins type cloud.api.src.routes, utiliser des chemins relatifs
from routes import user, dashboard

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(download_upload.router)
app.include_router(user.router)
app.include_router(dashboard.router)

templates = Jinja2Templates(directory="../templates")
print(CONFIG)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})
    #return RedirectResponse(url="/docs")


def run():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run()
