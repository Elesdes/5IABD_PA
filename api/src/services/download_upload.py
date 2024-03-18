from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from api.src.config import app_config as config
from api.src.utils.files_utils import is_valid_mime
import os
import zipfile


router = APIRouter(prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},)


@router.get("/{filename}")
def download(filename: str, request: Request):
    # TODO : retirer la ligne suivante une fois que l'on a automatisé l'envoi du nom de fichier
    filename: str = "FINALE.keras"
    return FileResponse(path=config.DOWNLOAD_PATH+config.SESSION_PATH+filename, filename=filename, media_type='application/octet-stream')


@router.post("/")
def upload(files: list[UploadFile] = File(...)):
    try:
        if not os.path.exists("./upload_fastapi"):
            os.makedirs("./upload_fastapi")

        for file in files:
            with zipfile.ZipFile(file.file, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    if is_valid_mime(member.filename):
                        zip_ref.extract(member, "./upload_fastapi")
                    else:
                        raise HTTPException(status_code=415, detail="Les fichiers doivent être de type PNG ou JPG.")

        return {"message": "Fichiers téléchargés avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
