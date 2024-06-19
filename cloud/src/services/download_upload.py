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
# Le traitement cotnenu à l'intérieur, par contre, peut rester ici
@router.get("/{idModel}")
# def download(filename: str = "FINALE.keras", request: Request = None):
def download_mymodels(request: Request, idModel: int) -> FileResponse:
    idModel = escape(idModel)
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_model_and_profile(request, cursor, idModel):
            current_user = User().get_user_by_cookie(cursor, cookie=escape(request.cookies.get("ICARUS-Login")))
            client = storage.Client()
            bucket = client.get_bucket("icarus-gcp.appspot.com")
            file_path = f"{idModel}.zip"
            blob = bucket.blob(f"{current_user.email}/{file_path}")
            blob.download_to_filename(file_path)
            return FileResponse(file_path, filename=f"{idModel}.zip")
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid profile.",
            )


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
            client = storage.Client()
            bucket = client.get_bucket("icarus-gcp.appspot.com")
            file_path = f"{files[0].filename}"
            blob = bucket.blob(f"{user.email}/{file_path}")
            blob.upload_from_filename(file_path)
        return {"message": "Fichiers téléchargés avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
