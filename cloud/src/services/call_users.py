from fastapi import APIRouter, status, HTTPException, Request, Form
from src.models.user_model import User
from src.utils.postgresql_utils import PostgreSQLUtils
from src.utils.files_utils import verify_role_and_profile
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
templates = Jinja2Templates(directory="./templates/")


@router.get("/get_profile")
def get_profile(request: Request) -> list[dict[str, str | list[str] | int]]:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        cookie = request.cookies.get("ICARUS-Login")
        if verify_role_and_profile(
            request, cursor, cookie=cookie
        ):
            SQL_query = "SELECT forename, name, email FROM USERS WHERE cookie=%s"
            cursor.execute(SQL_query, (cookie,))
            user_data = cursor.fetchall()
            # user_data = [dict(row) for row in user_data]
            users = []
            for user in user_data:
                users.append(
                    {
                        "forename": user[0],
                        "name": user[1],
                        "email": user[2]
                    }
                )
            return users
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.get("/get_users")
def get_users(request: Request) -> list[dict[str, str | list[str] | int]]:
    db_utils = PostgreSQLUtils()
    # Set the mail to "" because the verify_role_and_profile will fail the second test. Therefore, only an admin car get all users.
    email = ""
    users = []
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, email=email):
            SQL_query = "SELECT idusers, forename, name, email, role FROM USERS"
            cursor.execute(SQL_query)
            user_data = cursor.fetchall()
            # user_data = [dict(row) for row in user_data]
            for user in user_data:
                users.append(
                    {
                        "idUsers": user[0],
                        "forename": user[1],
                        "name": user[2],
                        "email": user[3],
                        "role": user[4],
                    }
                )
            return users
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.get("/get_role")
def get_role(request: Request) -> bool:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        cookie = request.cookies.get("ICARUS-Login")
        if verify_role_and_profile(request, cursor, cookie=cookie):
            SQL_query = "SELECT role FROM USERS where cookie=%s"
            cursor.execute(SQL_query, (cookie,))
            user_data = cursor.fetchone()
            if user_data[0] == 1:
                return True
            return False
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.delete("/del_users/{idUsers}", status_code=200)
def del_users(request: Request, idUsers: str) -> None:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = "DELETE FROM USERS WHERE idusers=%s"
            cursor.execute(SQL_query, (idUsers,))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.get("/del_profile/", status_code=200, response_class=HTMLResponse)
def del_profile(request: Request) -> HTMLResponse:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        cookie = request.cookies.get("ICARUS-Login")
        if verify_role_and_profile(
            request, cursor, cookie=cookie
        ):
            SQL_query = (
                "DELETE FROM USERS WHERE cookie=%s"
            )
            cursor.execute(SQL_query, (cookie,))
            return templates.TemplateResponse(
                name="index.html", context={"request": request}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.post("/update_users/")
def update_users(
    request: Request, idUsers: str, name: str, forename: str, email: str, role: str
) -> None:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            # If the request come from a User, he can't set the user_role to Admin.
            # Technically, he can't access the webpage to this, but he can still tinker the request himself.
            user_role = User().get_current_user_role(
                request.cookies.get("ICARUS-Login"), cursor
            )
            if user_role == 2:
                role = 2
            else:
                role = 1 if role == "Admin" else 2
            SQL_query = "UPDATE USERS SET name = %s, forename = %s, email = %s, role = %s WHERE idusers = %s"
            cursor.execute(SQL_query, (name, forename, email, role, idUsers))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )


# Very similar to the previous function but not called the same way. Thus, we shouldn't try a refacto.
@router.post("/update_profile", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    email: Annotated[str, Form()],
    forename: Annotated[str, Form()],
    name: Annotated[str, Form()],
    password: Optional[str] = Form(None),
) -> HTMLResponse:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        cookie = request.cookies.get('ICARUS-Login')
        if verify_role_and_profile(request, cursor, cookie=cookie):
            if password is None:
                SQL_query = "UPDATE USERS SET forename=%s, name=%s WHERE cookie=%s"
                cursor.execute(SQL_query, (forename, name, cookie))
            else:
                SQL_query = "UPDATE USERS SET forename=%s, name=%s, password=%s WHERE cookie=%s"
                cursor.execute(SQL_query, (forename, name, password, cookie))
            return templates.TemplateResponse(
                name="profile.html", context={"request": request}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )
