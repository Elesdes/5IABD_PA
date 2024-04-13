from fastapi import APIRouter, status, HTTPException, Request, Form
from models.user_model import User
from config.db_config import ConfigDB
from utils.files_utils import verify_role_and_profile
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, Annotated


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")
templates = Jinja2Templates(directory="../templates/")


@router.get("/get_profile")
def get_profile(request: Request) -> list[dict[str, str | list[str] | int]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if verify_role_and_profile(request, cursor, cookie=request.cookies.get("ICARUS-Login")):
        SQL_query = (
            f"SELECT forename, name, email FROM USERS WHERE cookie='{request.cookies.get('ICARUS-Login')}'"
        )
        cursor.execute(SQL_query)
        user_data = cursor.fetchall()
        user_data = [dict(row) for row in user_data]
        cursor.close()
        DB.connector.close()
        return user_data
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid profile.",
        )


@router.get("/get_users")
def get_users(request: Request) -> list[dict[str, str | list[str] | int]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    # Set the mail to "" because the verify_role_and_profile will fail the second test. Therefore, only an admin car get all users.
    email = ""
    users = []
    if verify_role_and_profile(request, cursor, email=email):
        SQL_query = (
            f"SELECT idusers, forename, name, email, role FROM USERS"
        )
        cursor.execute(SQL_query)
        user_data = cursor.fetchall()
        user_data = [dict(row) for row in user_data]
        for user in user_data:
            users.append({"idUsers": user["idusers"], "forename": user["forename"], "name": user["name"], "email": user["email"], "role": user["role"]})
        cursor.close()
        DB.connector.close()
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid profile.",
        )


@router.delete("/del_users/{idUsers}", status_code=200)
def del_users(request: Request, idUsers: str) -> None:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if verify_role_and_profile(request, cursor, id_users=idUsers):
        SQL_query = (
            f"DELETE FROM USERS WHERE idusers='{idUsers}'"
        )
        cursor.execute(SQL_query)
        DB.connector.commit()
        cursor.close()
        DB.connector.close()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid profile.",
        )


@router.post("/update_users/")
def update_users(request: Request, idUsers: str, name: str, forename: str, email: str, role: str) -> None:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if verify_role_and_profile(request, cursor, id_users=idUsers):
        # If the request come from a User, he can't set the user_role to Admin.
        # Technically, he can't access the webpage to this, but he can still tinker the request himself.
        user_role = User().get_current_user_role(request.cookies.get("ICARUS-Login"), cursor)
        if user_role == 2:
            role = 2
        else:
            role = 1 if role == "Admin" else 2
        SQL_query = (
            f"UPDATE USERS SET name = '{name}', forename = '{forename}', email = '{email}', role = '{role}' WHERE idusers = '{idUsers}'"
        )
        cursor.execute(SQL_query)
        DB.connector.commit()
        cursor.close()
        DB.connector.close()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


# Very similar to the previous function but not called the same way. Thus, we shouldn't try a refacto.
@router.post("/update_profile", response_class=HTMLResponse)
async def update_profile(request: Request, email: Annotated[str, Form()], forename: Annotated[str, Form()], name: Annotated[str, Form()], password: Optional[str] = Form(None)) -> HTMLResponse:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if verify_role_and_profile(request, cursor, email=email):
        if password is None:
            SQL_query = (
                f"UPDATE USERS SET forename='{forename}', name='{name}' WHERE cookie='{request.cookies.get('ICARUS-Login')}'"
            )
        else:
            SQL_query = (
                f"UPDATE USERS SET forename='{forename}', name='{name}', password='{password}' WHERE cookie='{request.cookies.get('ICARUS-Login')}'"
            )
        cursor.execute(SQL_query)
        DB.connector.commit()
        cursor.close()
        DB.connector.close()
        return templates.TemplateResponse(
            name="profile.html", context={"request": request}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid profile.",
        )
