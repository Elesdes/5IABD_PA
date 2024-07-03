from fastapi import Request, APIRouter, status, HTTPException
from markupsafe import escape
from src.models.device_model import DeviceModel
from src.models.user_model import User
from src.utils.postgresql_utils import PostgreSQLUtils
from src.utils.files_utils import verify_role_and_profile


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/link-device")
def link_device(request: Request, device: DeviceModel):
    db_session = PostgreSQLUtils()
    with db_session as cursor:
        user = User().get_user_by_cookie(
            cursor, cookie=escape(request.cookies.get("ICARUS-Login"))
        )

        cursor.execute(
            "SELECT IdUser FROM DEVICES WHERE IdDevice = %s", (device,)  # device.device_id,
        )
        if cursor.fetchone():
            # Device exists, only update the user
            cursor.execute(
                "UPDATE DEVICES SET IdUser = %s WHERE IdDevice = %s",
                (user.idusers, device),  # device.device_id,
            )
        else:
            # Device doesn't exist, insert a new record
            cursor.execute(
                "INSERT INTO DEVICES (IdDevice, IdUser) VALUES (%s, %s)",
                (device, user.idusers),  # device.device_id,
            )

    return {"message": "Prosthesis connected successfully"}


@router.post("/delete-device")
def delete_device(request: Request, device: str):
    db_session = PostgreSQLUtils()
    with db_session as cursor:
        user = User().get_user_by_cookie(
            cursor, cookie=escape(request.cookies.get("ICARUS-Login"))
        )

        cursor.execute(
            "SELECT IdUser FROM DEVICES WHERE IdDevice = %s", (device,)  # device.device_id,
        )
        result = cursor.fetchone()
        if result:
            if verify_role_and_profile(request, cursor, id_users=result[0]):
                # Device exists, only update the user
                cursor.execute(
                    "DELETE FROM DEVICES WHERE IdDevice = %s",
                    (device, )  # device.device_id,
                )
            else:
                return {"message": "Forbidden request"}
        else:
            return {"message": "Prosthesis doesn't exist"}

    return {"message": "Prosthesis connected successfully"}


@router.get("/get_devices")
def get_devices(request: Request) -> list[dict[str, str]]:
    db_utils = PostgreSQLUtils()
    devices = []
    # Set the mail to "" because the verify_role_and_profile will fail the second test. Therefore, only an admin car get all users.
    email = ""
    with db_utils as cursor:
        if verify_role_and_profile(request, cursor, email=email):
            SQL_query = "SELECT iddevice, iduser FROM DEVICES"
            cursor.execute(SQL_query)
            devices_data = cursor.fetchall()
            for device in devices_data:
                if device[1]:
                    devices.append(
                        {
                            "iddevice": device[0],
                            "iduser": device[1],
                            "statut": "Connecté"
                        }
                    )
                else:
                    devices.append(
                        {
                            "iddevice": device[0],
                            "iduser": "Pas d'id",
                            "statut": "Déconnecté"
                        }
                    )
            return devices
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid profile.",
            )
