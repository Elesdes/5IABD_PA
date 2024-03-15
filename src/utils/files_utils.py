import zipfile
import os
import logging


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
