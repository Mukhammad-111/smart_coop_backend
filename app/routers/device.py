from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import verify_api_key, get_db, get_current_user
from app.models import User
from app.schemas.device import DeviceResponse, DeviceStateRequest, DeviceStateResponse
from app.services.device_state import device_state_create_service, device_state_get_service

router = APIRouter(prefix="/device", tags=["Device"])


@router.post("/state", response_model=DeviceResponse)
async def device_state_create(data: DeviceStateRequest,
                              _: User = Depends(verify_api_key),
                              db: AsyncSession = Depends(get_db)):
    return await device_state_create_service(data, db)


@router.get("/state", response_model=DeviceStateResponse)
async def device_state_get(user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    return await device_state_get_service(db)