from models.user_model import User
from fastapi import Request
import psycopg2
import zipfile
import os
import logging


def is_valid_mime(file_name: str) -> bool:
    """
    Low security check of file extension.
    :param file_name: String of the file name.
    :return:
    If its a PNG or JPG, then it's true. Else it's false.
    """
    valid_extensions: list[str] = ['.png', '.jpg', '.jpeg']
    ext: str = os.path.splitext(file_name)[-1].lower()
    return ext in valid_extensions


def get_extension(file_path: str) -> str:
    """
    Get the extension of the specified file.
    """
    return os.path.splitext(file_path)[1]


def empty_file_content(*, file_path: str) -> None:
    try:
        open(file_path, "w").close()

        logging.info(f"File content emptied: {file_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error emptying file content: {e}")


def generate_zip_file(*, input_file_path: str, output_file_path: str) -> None:
    """
    Generate a zip file from the specified file.
    """
    try:
        with zipfile.ZipFile(output_file_path, "w") as zipf:
            zipf.write(input_file_path, arcname=os.path.basename(input_file_path))
    except FileNotFoundError:
        logging.error(f"File not found: {input_file_path}")
    except Exception as e:
        logging.error(f"Error generating ZIP archive: {e}")


def verify_role_and_profil(request: Request, cursor: psycopg2, id_users: int = None, email: str = None, cookie: str = None) -> bool:
    """
    Used in order to check the privileges of the current user.
    :param request: request metadata of the user
    :param cursor: cursor of the BDD
    :param id_users: id of the user
    :param email: email of the user
    :param cookie: cookie registered in the BDD of the user
    :return:
    True if the user is allowed. False if not.
    """
    current_user = User().get_user(cursor, cookie=request.cookies.get("ICARUS-Login"))
    request_target = User().get_user(cursor, id_users=id_users, email=email, cookie=cookie)
    if current_user.role == 1 or current_user.email == request_target.email:
        return True
    return False
