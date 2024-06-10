from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.config import app_config as config
from src.utils.files_utils import is_valid_mime, verify_model_and_profile
from src.utils.postgresql_utils import PostgreSQLUtils
from src.models.user_model import User
from google.cloud import storage
import os
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
    db_utils = PostgreSQLUtils()
    with db_utils as cursor:
        if verify_model_and_profile(request, cursor, idModel):
            current_user = User().get_user(cursor, cookie=request.cookies.get("ICARUS-Login"))
            client = storage.Client()
            bucket = client.get_bucket("icarus-gcp.appspot.com")
            file_path = f"{current_user.email}/{idModel}.zip"
            blob = bucket.blob(file_path)
            blob.download_to_filename(file_path)
            return FileResponse(file_path, filename=f"{idModel}.zip")
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid profile.",
            )


@router.post("/")
def upload(files: list[UploadFile] = File(...)):
    try:
        if not os.path.exists("./upload_fastapi"):
            os.makedirs("./upload_fastapi")

        for file in files:
            # Attention à utiliser une méthode de compression -> https://docs.python.org/3/library/zipfile.html#zipfile-objects
            # with zipfile.ZipFile(file.file, "r", compression=zipfile.ZIP_DEFLATED) as zip_ref:
            # Eventuellement, ajouter la fonction de création de zip dans le fichier utils/files_utils.py
            with zipfile.ZipFile(file.file, "r") as zip_ref:
                for member in zip_ref.infolist():
                    if is_valid_mime(member.filename):
                        zip_ref.extract(member, "./upload_fastapi")
                    else:
                        raise HTTPException(
                            status_code=401,
                            detail="Les fichiers doivent être de type PNG ou JPG.",
                        )

        return {"message": "Fichiers téléchargés avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
