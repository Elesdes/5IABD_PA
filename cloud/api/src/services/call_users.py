from fastapi import APIRouter
from config.db_config import ConfigDB


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_users")
def get_users() -> list[dict[str, str | list[str] | int]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    users = []
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


@router.delete("/del_users/{idUsers}")
def del_users(idUsers: str) -> None:
    # Todo : On doit impérativement vérifier le rôle de l'utilisateur avec le cookie. Seuls les admins ont le droit.
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    SQL_query = (
        f"DELETE FROM USERS WHERE idusers='{idUsers}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()

@router.post("/update_users/")
def update_users(idUsers: str, name: str, forename: str, email: str, role: str) -> None:
    # TODO : Attention aux cookies!
    role = 1 if role == "Admin" else 2
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    SQL_query = (
        f"UPDATE USERS SET name = '{name}', forename = '{forename}', email = '{email}', role = '{role}' WHERE idusers = '{idUsers}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()
