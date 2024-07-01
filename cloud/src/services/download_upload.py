from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.config import app_config as config
from src.utils.files_utils import is_valid_mime, verify_model_and_profile
from src.utils.postgresql_utils import PostgreSQLUtils
from src.models.user_model import User
from google.cloud import storage
from markupsafe import escape
import zipfile


router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


# Ce sont des routes, elles doivent être dans un fichier routes.
# Le traitement contenu à l'intérieur, par contre, peut rester ici
@router.get("/{idDevice}")
def download_mymodels(idDevice: str) -> FileResponse:
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
        blob = bucket.blob(f"{user_data[0]}/{model_data[0]}")
        blob.download_to_filename(f"/tmp/{model_data[0]}")
        return FileResponse(f"/tmp/{model_data[0]}", filename=f"{model_data[0]}")


@router.post("/")
def upload(request: Request, files: list[UploadFile] = File(...)):
    if len(files) > 2:
        raise HTTPException(
            status_code=401,
            detail="Un seul upload possible.",
        )
    try:
        # Eventuellement, ajouter la fonction de création de zip dans le fichier utils/files_utils.py
        with zipfile.ZipFile(files[0].file, "r") as zip_ref:
            for member in zip_ref.infolist():
                if not is_valid_mime(member.filename):
                    raise HTTPException(
                        status_code=401,
                        detail="Les fichiers doivent être de type csv.",
                    )
        db_utils = PostgreSQLUtils()
        with db_utils as cursor:
            user = User().get_user_by_cookie(cursor=cursor, cookie=escape(request.cookies.get("ICARUS-Login")))
            if user:
                client = storage.Client()
                bucket = client.get_bucket("icarus-gcp.appspot.com")
                file_path = f"{files[0].filename}"
                blob = bucket.blob(f"{user.idusers}/{file_path}")
                blob.upload_from_filename(file_path)
            else:
                return {"message": "Pas d'utilisateurs avec vos données d'identifications."}
        return {"message": "Fichiers téléchargés avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
