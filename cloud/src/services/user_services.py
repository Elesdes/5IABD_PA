from fastapi import Request
from fastapi.responses import HTMLResponse
from src.utils.postgresql_utils import PostgreSQLUtils
from src.models.user_model import User
from src.services.cookie_services import set_cookie, set_response_cookie
from passlib.context import CryptContext
import psycopg2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def request_dashboard(request: Request) -> bool:
    cookie_value = request.cookies.get("ICARUS-Login")
    if cookie_value is not None:
        db_utils = PostgreSQLUtils()
        with db_utils as cursor:
            if User().get_user(cursor, cookie=cookie_value) is not None:
                return True
    return False


def request_admin(request: Request) -> bool:
    cookie_value = request.cookies.get("ICARUS-Login")
    if cookie_value is not None:
        db_utils = PostgreSQLUtils()
        with db_utils as cursor:
            user = User().get_user(cursor, cookie=cookie_value)
            if user is not None and user.role == 1:
                return True
    return False


def request_login(
    email: str, password: str
) -> User | None:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        user = User().get_user(cursor, email=email)
        if not user or not user.verify_password(password):
            return None
        user = set_cookie(user, cursor, email)
    return user


def request_register(
    request: Request,
    email: str,
    password: str,
    name: str,
    forename: str,
) -> HTMLResponse | None:
    user = User()
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if user.get_user(cursor, email=email) is not None:
            return None
        user = user.insert_user(
            cursor,
            email,
            pwd_context.hash(password),
            name,
            forename,
        )
    return set_response_cookie(request, "dashboard.html", user.cookie)
