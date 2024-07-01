import datetime
from fastapi import APIRouter, status, HTTPException, Request
from src.utils.postgresql_utils import PostgreSQLUtils
from src.utils.files_utils import verify_role_and_profile
from src.services.update_storage import delete_model
from markupsafe import escape
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_models")
def get_models(request: Request) -> list[dict[str, str | datetime | int]]:
    db_utils = PostgreSQLUtils()
    models = []
    # Set the mail to "" because the verify_role_and_profile will fail the second test. Therefore, only an admin car get all users.
    email = ""
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, email=email):
            SQL_query = "SELECT idmodel, path, date, idusers FROM MODELS"
            cursor.execute(SQL_query)
            model_data = cursor.fetchall()
            # model_data = [dict(row) for row in model_data]
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
    idUsers = escape(idUsers)
    db_utils = PostgreSQLUtils()
    models = []
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = (
                "SELECT idmodel, path, date, email FROM MODELS WHERE idUsers=%s"
            )
            cursor.execute(SQL_query, (idUsers,))
            model_data = cursor.fetchall()
            # model_data = [dict(row) for row in model_data]
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
def get_mymodel(request: Request) -> list[dict[str, str | datetime | int]]:
    db_utils = PostgreSQLUtils()
    models = []
    cookie_value = escape(request.cookies.get("ICARUS-Login"))
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, cookie=cookie_value):
            SQL_query = "SELECT idusers FROM USERS WHERE cookie=%s"
            cursor.execute(SQL_query, (cookie_value,))
            SQL_query = "SELECT idmodel, path, date FROM MODELS WHERE idUsers=%s"
            cursor.execute(SQL_query, (cursor.fetchone()[0],))
            model_data = cursor.fetchall()
            # model_data = [dict(row) for row in model_data]
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
    idUsers = escape(idUsers)
    idModel = escape(idModel)
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = "SELECT path FROM MODELS WHERE idModel=%s"
            cursor.execute(SQL_query, (idModel,))
            result = cursor.fetchone()
            SQL_query = "DELETE FROM MODELS WHERE idModel=%s"
            cursor.execute(SQL_query, (idModel,))
            delete_model(idUsers, result[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.delete("/del_mymodels/")
def del_mymodels(request: Request, idModel: int) -> None:
    idModel = escape(idModel)
    db_utils = PostgreSQLUtils()
    # cookie_value = request.cookies.get("ICARUS-Login")
    SQL_query = "SELECT idusers, path FROM MODELS WHERE idmodel=%s"
    with db_utils as cursor:
        cursor.execute(SQL_query, (idModel,))
        result = cursor.fetchone()
        if verify_role_and_profile(request, cursor, id_users=result[0]):
            SQL_query = "DELETE FROM MODELS WHERE idModel=%s"
            cursor.execute(SQL_query, (idModel,))
            delete_model(result[0], result[1])
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.post("/update_model/")
def update_model(
    request: Request, idModel: str, path: str, date: datetime, idUsers: str
) -> None:
    idModel = escape(idModel)
    path = escape(path)
    date = escape(date)
    idUsers = escape(idUsers)
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = "UPDATE MODELS SET path = %s, date = %s, idusers = %s WHERE idModel = %s"
            cursor.execute(SQL_query, (path, date, idUsers, idModel))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.post("/take_model/")
def take_model(
    request: Request, idModel: str, idUsers: str
) -> None:
    idModel = escape(idModel)
    date = datetime.now()
    idUsers = escape(idUsers)
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, id_users=idUsers):
            SQL_query = "UPDATE MODELS SET date = %s WHERE idModel = %s"
            cursor.execute(SQL_query, (date, idModel))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )


@router.post("/take_mymodel/")
def take_mymodel(
    request: Request, idModel: str
) -> None:
    idModel = escape(idModel)
    date = datetime.now()
    cookie = escape(request.cookies.get("ICARUS-Login"))
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, cookie=cookie):
            SQL_query = "UPDATE MODELS SET date = %s WHERE idModel = %s"
            print(SQL_query, (date, idModel))
            cursor.execute(SQL_query, (date, idModel))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )