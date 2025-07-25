from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from src.models.user_model import User
import psycopg2
import string
import random
from datetime import timedelta, timezone, datetime


templates = Jinja2Templates(directory="./templates/")


def set_response_cookie(
    request: Request, web_page: str, cookie_value: str
) -> HTMLResponse:
    expiry = datetime.now(timezone.utc) + timedelta(days=1)
    response = templates.TemplateResponse(
        name=f"{web_page}", context={"request": request}
    )
    response.set_cookie(
        key="ICARUS-Login",
        value=f"{cookie_value}",
        expires=expiry,
        secure=True,
        samesite="strict",
    )
    return response


def set_cookie(user: User, cursor: psycopg2, email: str) -> User:
    letters = string.ascii_lowercase
    cookie_value = "".join(random.choice(letters) for _ in range(255))
    user.set_cookie(cursor, email, cookie_value)
    return user
