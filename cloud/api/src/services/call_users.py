from typing import Dict, Any, List

from fastapi import APIRouter, Request
from config.db_config import ConfigDB


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_users")
def get_users() -> list[dict[str, str | list[str]]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    users = []
    SQL_query = (
        f"SELECT forename, name, email, role FROM USERS"
    )
    cursor.execute(SQL_query)
    user_data = cursor.fetchall()
    user_data = [dict(row) for row in user_data]
    for user in user_data:
        users.append({"forename": user["forename"], "name": user["name"], "email": user["email"], "role": "User" if user["role"] == 2 else "Admin"})
    cursor.close()
    DB.connector.close()
    return users


@router.delete("/del_users/{email_id}")
def del_users(email_id: str):
    # Todo : On doit impérativement vérifier le rôle de l'utilisateur avec le cookie. Seuls les admins ont le droit.
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    users = []
    SQL_query = (
        f"DELETE FROM USERS WHERE email='{email_id}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()
