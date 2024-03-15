from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .config.app_config import CONFIG

app = FastAPI()
print(CONFIG)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
