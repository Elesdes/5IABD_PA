from typing import Any

from fastapi import APIRouter, Request
from models.device_model import DeviceModel
from services.devices_services import link_device

router = APIRouter(
    prefix="/devices", tags=["devices"], responses={404: {"description": "Not found"}}
)


@router.get("/link-device/")
async def link_device(request: Request, device: DeviceModel) -> Any:
    return link_device(request, device)
