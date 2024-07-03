from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from starlette.background import BackgroundTask
from src.utils.files_utils import is_valid_mime, verify_model_and_profile
from src.utils.postgresql_utils import PostgreSQLUtils
from src.models.user_model import User
from src.services.call_models import add_model
from google.cloud import storage
from markupsafe import escape
from io import BytesIO
import zipfile
import os


router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


def file_generator(file_path: str):
    with open(file_path, "rb") as file:
        yield from file


def remove_file(file_path: str):
    os.remove(file_path)


# Ce sont des routes, elles doivent être dans un fichier routes.
# Le traitement contenu à l'intérieur, par contre, peut rester ici
@router.get("/{idDevice}")
def download_mymodels(idDevice: str) -> StreamingResponse:
    idDevice = escape(idDevice)
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        cursor.execute(
            "SELECT IdUser FROM DEVICES WHERE IdDevice = %s", (idDevice, )
        )
        user_data = cursor.fetchone()
        if not user_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid profile.",
            )
        cursor.execute(
            "SELECT path FROM MODELS WHERE idUsers = %s ORDER BY date DESC LIMIT 1", (user_data[0],)
        )
        model_data = cursor.fetchone()
        if not model_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid profile.",
            )
        client = storage.Client()
        bucket = client.get_bucket("icarus-gcp.appspot.com")
        # file_path = f"PPO_hand_prosthesis_model.zip"
        user_id = user_data[0].replace('/', '\\')
        blob = bucket.blob(f"{user_id}/{model_data[0]}")
        blob.download_to_filename(f"/tmp/{model_data[0]}")

        response = StreamingResponse(file_generator(f"/tmp/{model_data[0]}"), media_type="application/octet-stream")
        response.headers["Content-Disposition"] = f"attachment; filename={model_data[0]}"
        # Add background task to remove the file after the response is sent
        response.background = BackgroundTask(remove_file, f"/tmp/{model_data[0]}")
        return response


@router.post("/")
def upload(request: Request, files: list[UploadFile] = File(...)):
    if len(files) > 2:
        raise HTTPException(
            status_code=401,
            detail="Un seul upload possible.",
        )
    # Eventuellement, ajouter la fonction de création de zip dans le fichier utils/files_utils.py
    with zipfile.ZipFile(files[0].file, "r") as zip_ref:
        db_utils = PostgreSQLUtils()
        with db_utils as cursor:
            user = User().get_user_by_cookie(cursor=cursor, cookie=escape(request.cookies.get("ICARUS-Login")))
            for member in zip_ref.infolist():
                if not is_valid_mime(member.filename):
                    raise HTTPException(
                        status_code=401,
                        detail="Les fichiers doivent être de type pkl.",
                    )
                if user:
                    file_data = zip_ref.read(member)
                    client = storage.Client()
                    bucket = client.get_bucket("icarus-gcp.appspot.com")
                    file_path = f"{member.filename}"
                    user_id = user.idusers.replace('/', '\\')
                    blob = bucket.blob(f"{user_id}/{file_path}")
                    blob.upload_from_file(BytesIO(file_data), content_type='application/octet-stream')
                    add_model(request, file_path, user.idusers)
                else:
                    return {"message": "Pas d'utilisateurs avec vos données d'identifications."}
    return {"message": "Fichiers uploadé avec succès."}

