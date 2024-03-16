from fastapi import FastAPI
from starlette.responses import RedirectResponse
import uvicorn

from config.app_config import CONFIG

app = FastAPI()
print(CONFIG)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


def run():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run()
