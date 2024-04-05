from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, HTMLResponse
import uvicorn
from starlette.templating import Jinja2Templates

from config.app_config import CONFIG
from api.src.services import download_upload
from api.src.routes import pages

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(download_upload.router)
app.include_router(pages.router)
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
