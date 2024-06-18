from src.models.user_model import User
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
    valid_extensions: list[str] = [".csv"]
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


def verify_role_and_profile(
    request: Request,
    cursor: psycopg2,
    id_users: int = None,
    email: str = None,
    cookie: str = None,
) -> bool:
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
    current_user = User().get_user_by_cookie(cursor, cookie=request.cookies.get("ICARUS-Login"))
    print(current_user)
    # First check to determine if we only need to check the role. Else request_target.email will make a runtime error.
    if current_user.role == 2 and email == "":
        return False
    request_target = None
    if id_users:
        request_target = User().get_user_by_id(cursor, id_users=id_users)
    if email:
        request_target = User().get_user_by_email(cursor, email=email)
    if cookie:
        request_target = User().get_user_by_cookie(cursor, cookie=cookie)
    if request_target is None:
        return False
    if current_user.role == 1 or current_user.email == request_target.email:
        return True
    return False


def verify_model_and_profile(
    request: Request,
    cursor: psycopg2,
    id_model: int = None,
) -> bool:
    """
    Used in order to check if the model belongs to the current user or if he is an admin.
    :param request: request metadata of the user
    :param cursor: cursor of the BDD
    :param id_users: id of the user
    :param email: email of the user
    :param cookie: cookie registered in the BDD of the user
    :return:
    True if the user is allowed. False if not.
    """
    current_user = User().get_user_by_cookie(cursor, cookie=request.cookies.get("ICARUS-Login"))
    if current_user.role == 1:
        return True
    SQL_query =( "SELECT idmodel FROM MODELS WHERE idmodel = %s AND idusers = %s" )
    cursor.execute(SQL_query, (id_model, current_user.id))
    model_data = cursor.fetchall()
    if model_data:
        return False
    return True
