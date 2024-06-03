from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.config import app_config as config
from src.utils.files_utils import is_valid_mime
import os
import zipfile


router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


# Ce sont des routes, elles doivent être dans un fichier routes.
# Le traitement cotnenu à l'intérieur, par contre, peut rester ici
@router.get("/{filename}")
# def download(filename: str = "FINALE.keras", request: Request = None):
def download(filename: str, request: Request):
    # TODO : retirer la ligne suivante une fois que l'on a automatisé l'envoi du nom de fichier
    filename: str = "FINALE.keras"
    # path_to_file = config.DOWNLOAD_PATH + config.SESSION_PATH + filename
    # return FileResponse(path=path_to_file, filename=filename, media_type='application/octet-stream')
    return FileResponse(
        path=config.DOWNLOAD_PATH + config.SESSION_PATH + filename,
        filename=filename,
        media_type="application/octet-stream",
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
                            status_code=415,
                            detail="Les fichiers doivent être de type PNG ou JPG.",
                        )

        return {"message": "Fichiers téléchargés avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
