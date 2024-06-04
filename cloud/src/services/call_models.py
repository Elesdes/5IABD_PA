import datetime
from fastapi import APIRouter, status, HTTPException, Request
from src.utils.postgresql_utils import PostgreSQLUtils
from src.utils.files_utils import verify_role_and_profile


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_models")
def get_models(request: Request) -> list[dict[str, str | datetime.datetime | int]]:
    db_utils = PostgreSQLUtils()
    models = []
    # Set the mail to "" because the verify_role_and_profile will fail the second test. Therefore, only an admin car get all users.
    email = ""
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, email=email):
            SQL_query = f"SELECT idmodel, path, date, idusers FROM MODELS"
            cursor.execute(SQL_query)
            model_data = cursor.fetchall()
            model_data = [dict(row) for row in model_data]
            for model in model_data:
                models.append(
                    {
                        "idModel": model[0],
                        "path": model[1],
                        "date": model[2],
                        "idUsers": model[3],
                    }
                )
            return models
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.get("/get_model/{idUsers}")
def get_model(request: Request, idUsers: str) -> list[dict[str, str | list[str]]]:
    db_utils = PostgreSQLUtils()
    models = []
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = (
                f"SELECT idmodel, path, date, email FROM MODELS WHERE idUsers='{idUsers}'"
            )
            cursor.execute(SQL_query)
            model_data = cursor.fetchall()
            model_data = [dict(row) for row in model_data]
            for model in model_data:
                models.append(
                    {
                        "idModel": model[0],
                        "path": model[1],
                        "date": model[2],
                        "idUsers": idUsers,
                    }
                )
            return models
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.get("/get_mymodel/")
def get_mymodel(request: Request) -> list[dict[str, str | datetime.datetime | int]]:
    db_utils = PostgreSQLUtils()
    models = []
    cookie_value = request.cookies.get("ICARUS-Login")
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, cookie=cookie_value):
            SQL_query = f"SELECT idusers FROM USERS WHERE cookie='{cookie_value}'"
            cursor.execute(SQL_query)
            SQL_query = f"SELECT idmodel, path, date FROM MODELS WHERE idUsers='{cursor.fetchone()[0]}'"
            cursor.execute(SQL_query)
            model_data = cursor.fetchall()
            model_data = [dict(row) for row in model_data]
            for model in model_data:
                models.append(
                    {
                        "idModel": model[0],
                        "path": model[1],
                        "date": model[2],
                    }
                )
            return models
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.delete("/del_models/")
def del_models(request: Request, idUsers: str, idModel: int) -> None:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = f"DELETE FROM MODELS WHERE idModel='{idModel}'"
            cursor.execute(SQL_query)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.delete("/del_mymodels/")
def del_mymodels(request: Request, idModel: int) -> None:
    db_utils = PostgreSQLUtils()
    cookie_value = request.cookies.get("ICARUS-Login")
    SQL_query = f"SELECT idusers FROM MODELS WHERE idmodel='{idModel}'"
    with db_utils as cursor:
        cursor.execute(SQL_query)
        if verify_role_and_profile(request, cursor, id_users=cursor.fetchone()[0]):
            SQL_query = f"DELETE FROM MODELS WHERE idModel='{idModel}'"
            cursor.execute(SQL_query)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.post("/update_model/")
def update_model(
    request: Request, idModel: str, path: str, date: datetime.datetime, idUsers: str
) -> None:
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = f"UPDATE MODELS SET path = '{path}', date = '{date}', idusers = '{idUsers}' WHERE idModel = '{idModel}'"
            cursor.execute(SQL_query)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )
