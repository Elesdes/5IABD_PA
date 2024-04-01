from typing import Annotated

from fastapi import FastAPI, Request, UploadFile, File, HTTPException, APIRouter, status, Depends, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from ..config.db_config import ConfigDB
import os
import psycopg2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/pages",
    tags=["pages"],
    responses={404: {"description": "Not found"}},)
templates = Jinja2Templates(directory="../templates/")
security = HTTPBasic()


class User:
    def __init__(self, email, name, forename, password, role):
        self.email = email
        self.name = name
        self.forename = forename
        self.password = password
        self.role = role

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)


def get_user(email, cursor):
    cursor.execute("SELECT email, name, forename, password, role FROM USERS WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data['email'], user_data['name'], user_data['forename'], user_data['password'], user_data['role'])
    return None


def get_current_user_role(email: str, cursor=Depends(ConfigDB().get_db_cursor())):
    user = get_user(email, cursor)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.role


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        name="about.html", context={"request": request}
    )


@router.get("/login", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        name="login.html", context={"request": request}
    )

"""
@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    user = get_user(credentials.username, cursor)

    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    cursor.close()
    DB.connector.close()

    return {"email": user.email, "role": user.role}
"""

@router.post("/login")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    user = get_user(email, cursor)

    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    cursor.close()
    DB.connector.close()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail={"email": user.email, "role": user.role},
        headers={"WWW-Authenticate": "Basic"},
    )

