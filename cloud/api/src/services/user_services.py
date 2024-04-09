from fastapi import Request
from config.db_config import ConfigDB
from models.user_model import User
from services.cookie_services import set_cookie, set_response_cookie
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")


def request_dashboard(request: Request) -> bool:
    cookie_value = request.cookies.get("ICARUS-Login")
    if cookie_value is not None:
        DB = ConfigDB()
        cursor = DB.get_db_cursor()
        if User().get_user(cursor, cookie=cookie_value) is not None:
            cursor.close()
            DB.connector.close()
            return True
        cursor.close()
        DB.connector.close()
    return False


def request_login(email: str, password: str) -> User | None:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    user = User().get_user(cursor, email=email)
    if not user or not user.verify_password(password):
        return None
    user = set_cookie(user, DB, email)
    cursor.close()
    DB.connector.close()
    return user


def request_register(request: Request, email: str, password: str, name: str, forename: str):
    user = User()
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    if user.get_user(cursor, email=email) is not None:
        return None
    user = user.insert_user(DB.connector, cursor, email, pwd_context.hash(password, scheme="md5_crypt"), name, forename)
    cursor.close()
    DB.connector.close()
    return set_response_cookie(request, "dashboard.html", user.cookie)
