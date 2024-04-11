import datetime

from fastapi import APIRouter
from config.db_config import ConfigDB


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_models")
def get_models() -> list[dict[str, str | datetime.datetime | int]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    models = []
    SQL_query = (
        f"SELECT idmodel, path, date, idusers FROM MODEL"
    )
    cursor.execute(SQL_query)
    model_data = cursor.fetchall()
    model_data = [dict(row) for row in model_data]
    for model in model_data:
        models.append({"idModel": model["idmodel"], "path": model["path"], "date": model["date"], "idUsers": model["idusers"]})
    cursor.close()
    DB.connector.close()
    return models


@router.get("/get_model/{idUsers}")
def get_model(idUsers: str) -> list[dict[str, str | list[str]]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    models = []
    SQL_query = (
        f"SELECT idmodel, path, date, email FROM MODEL WHERE idUsers='{idUsers}'"
    )
    cursor.execute(SQL_query)
    model_data = cursor.fetchall()
    model_data = [dict(row) for row in model_data]
    for model in model_data:
        models.append({"idModel": model["idmodel"], "path": model["path"], "date": model["date"], "idUsers": model["idusers"]})
    cursor.close()
    DB.connector.close()
    return models


@router.delete("/del_models/")
def del_models(idUsers: str, idModel: int) -> None:
    # Todo : On doit impérativement vérifier le rôle de l'utilisateur avec le cookie et le mail.
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    SQL_query = (
        f"DELETE FROM MODEL WHERE idModel='{idModel}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()


@router.post("/update_model/")
def update_model(idModel: str, path: str, date: datetime.datetime, idUsers: str) -> None:
    # TODO : Attention aux cookies!
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    SQL_query = (
        f"UPDATE MODEL SET path = '{path}', date = '{date}', idusers = '{idUsers}' WHERE idModel = '{idModel}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()
