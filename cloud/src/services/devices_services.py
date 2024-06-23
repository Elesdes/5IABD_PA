from fastapi import Request
from markupsafe import escape
from src.models.device_model import DeviceModel
from src.models.user_model import User
from src.utils.postgresql_utils import PostgreSQLUtils


def link_device(request: Request, device: DeviceModel):
    db_session = PostgreSQLUtils()
    with db_session as cursor:
        user = User().get_user_by_cookie(
            cursor, cookie=escape(request.cookies.get("ICARUS-Login"))
        )

        cursor.execute(
            "SELECT IdUser FROM DEVICES WHERE IdDevice = %s", (device.device_id,)
        )
        if device := cursor.fetchone():
            # Device exists, only update the user
            cursor.execute(
                "UPDATE DEVICES SET IdUser = %s WHERE IdDevice = %s",
                (user.get("id_user", "email"), device.device_id),
            )
        else:
            # Device doesn't exist, insert a new record
            cursor.execute(
                "INSERT INTO DEVICES (IdDevice, IdUser) VALUES (%s, %s)",
                (device.device_id, user.get("id_user", "email")),
            )

    return {"message": "Prosthesis connected successfully"}
