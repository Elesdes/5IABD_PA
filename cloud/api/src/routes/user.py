import datetime
from typing import Annotated

from fastapi import (
    Request,
    HTTPException,
    APIRouter,
    status,
    Depends,
    Form,
    Cookie,
    Response,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from passlib.hash import md5_crypt
from config.db_config import ConfigDB
from datetime import timezone, timedelta
import os
import psycopg2
import string
import random

# TODO Add salt mandatory
pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="../templates/")


# A mettre dans models/user.py
class User:
    def __init__(self, email, password, name, forename, role, cookie):
        self.email = email
        self.password = password
        self.name = name
        self.forename = forename
        self.role = role
        self.cookie = cookie

    def verify_password(self, plain_password):
        parts = self.password.split("$")
        scheme, salt, stored_hash = parts[1], parts[2], parts[3]
        stored_hash = stored_hash.strip()
        new_hash = md5_crypt.using(salt=salt).hash(plain_password)
        return new_hash == f"${scheme}${salt}${stored_hash}"


# Mettre les fonctions ci-dessous en tant que méthode de la classe User et ne pas oublier de typer
def get_user(cursor, email=None, cookie=None):
    SQL_query = (
        f"SELECT email, password, name, forename, role, cookie FROM USERS WHERE 1 = 1"
    )
    if email is not None:
        SQL_query += f" AND email = '{email}' "
    if cookie is not None:
        SQL_query += f" AND cookie = '{cookie}'"
    cursor.execute(SQL_query)
    user_data = cursor.fetchone()
    print(SQL_query)
    if user_data:
        return User(
            user_data["email"],
            user_data["password"],
            user_data["name"],
            user_data["forename"],
            user_data["role"],
            user_data["cookie"],
        )
    return None


def insert_user(connector, cursor, email, password, name, forename):
    cursor.execute(
        f"INSERT INTO users(email, password, name, forename, role, cookie) VALUES('{email}', '{password}', '{name}', '{forename}', 2, '')"
    )
    connector.commit()
    letters = string.ascii_lowercase
    cookie_value = "".join(random.choice(letters) for _ in range(255))
    set_cookie(connector, cursor, email, cookie_value)
    return User(email, password, name, forename, 2, cookie_value)


def get_current_user_role(email: str, cursor=Depends(ConfigDB().get_db_cursor())):
    user = get_user(cursor, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user.role


def set_cookie(connector, cursor, email, cookie_value):
    sql = f"UPDATE USERS SET cookie = '{cookie_value}' WHERE email = '{email}'"
    cursor.execute(sql)
    connector.commit()


# Tout ce qui est ici doit rester
# Attention cependant, le contenu des fonctions dashboard, register et login doivent être mis dans services/user_services.py
# Les routes ne doivent qu'être une simple redirection vers les fonctions de services (un peu comme ce qui est fait pour about, logout...)
@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(name="about.html", context={"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    cookie_value = request.cookies.get("ICARUS-Login")
    print(cookie_value)
    if cookie_value is not None:
        DB = ConfigDB()
        cursor = DB.get_db_cursor()
        if get_user(cursor, cookie=cookie_value) is not None:
            cursor.close()
            DB.connector.close()
            return templates.TemplateResponse(
                name="dashboard.html", context={"request": request}
            )
        cursor.close()
        DB.connector.close()
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/login", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/logout", response_class=HTMLResponse)
def logout(response: Response, request: Request):
    response.delete_cookie(key="ICARUS-Login")
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.get("/register", response_class=HTMLResponse)
async def create_user(request: Request):
    return templates.TemplateResponse(
        name="register.html", context={"request": request}
    )


@router.post("/register", response_class=HTMLResponse)
async def register(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    forename: Annotated[str, Form()],
    response: Response,
    request: Request,
):
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if get_user(cursor, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User already exists"
        )
    user = insert_user(
        DB.connector,
        cursor,
        email,
        pwd_context.hash(password, scheme="md5_crypt"),
        name,
        forename,
    )
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    cursor.close()
    DB.connector.close()
    expiry = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    response.set_cookie(
        key="ICARUS-Login",
        value=f"{user.cookie}",
        expires=expiry,
        secure=True,
        samesite="none",
    )
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response,
    request: Request,
):
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    user = get_user(cursor, email)
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    letters = string.ascii_lowercase
    cookie_value = "".join(random.choice(letters) for _ in range(255))
    set_cookie(DB.connector, cursor, email, cookie_value)
    cursor.close()
    DB.connector.close()
    expiry = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=1)
    response.set_cookie(
        key="ICARUS-Login",
        value=f"{cookie_value}",
        expires=expiry,
        secure=True,
        samesite="none",
    )
    return templates.TemplateResponse(
        name="dashboard.html", context={"request": request}
    )
