from pydantic import BaseModel, field_validator


class DeviceModel(BaseModel):
    device_id: str

    @field_validator("device_id")
    def validate_id_format(cls, device_id: str):
        if not device_id.isdigit() or len(device_id) != 8:
            raise ValueError("ID must be exactly 8 digits")
        return device_id
