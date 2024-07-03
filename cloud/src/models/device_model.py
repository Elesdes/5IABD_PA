from pydantic import BaseModel, field_validator
import re


class DeviceModel(BaseModel):
    device_id: str

    @field_validator("device_id")
    def validate_id_format(cls, device_id: str):
        try:
            print(device_id)
            pattern = re.compile(r'^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$')
            if not pattern.match(device_id):
                raise ValueError("ID must be exactly 19 digits with 3 -")
            return device_id
        except Exception as e:
            raise Exception(e)
