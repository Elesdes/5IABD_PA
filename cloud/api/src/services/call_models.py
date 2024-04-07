from fastapi import APIRouter
from config.db_config import ConfigDB


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_models")
def get_models() -> list[dict[str, str | list[str]]]:
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    models = []
    SQL_query = (
        f"SELECT path, date, email FROM MODEL"
    )
    cursor.execute(SQL_query)
    model_data = cursor.fetchall()
    model_data = [dict(row) for row in model_data]
    for model in model_data:
        models.append({"path": model["path"], "date": model["date"], "email": model["email"]})
    cursor.close()
    DB.connector.close()
    return models


@router.delete("/del_models/{date}&{email}")
def del_models(date: str, email: str):
    # Todo : On doit impérativement vérifier le rôle de l'utilisateur avec le cookie.
    DB = ConfigDB()
    cursor = DB.get_db_cursor()
    SQL_query = (
        f"DELETE FROM MODELS WHERE date='{date}' AND email='{email}'"
    )
    cursor.execute(SQL_query)
    DB.connector.commit()
    cursor.close()
    DB.connector.close()
