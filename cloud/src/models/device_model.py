from pydantic import BaseModel, field_validator


class DeviceModel(BaseModel):
    device_id: str

    @field_validator("id")
    def validate_id_format(cls, id: str):
        if not id.isdigit() or len(id) != 8:
            raise ValueError("ID must be exactly 8 digits")
        return id
