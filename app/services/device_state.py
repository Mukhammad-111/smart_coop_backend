from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DeviceState
from app.repositories.device_state import DeviceStateRepository
from app.schemas.device import DeviceStateRequest, DeviceResponse


async def device_state_create_service(data: DeviceStateRequest, db: AsyncSession):
    new_device_state = DeviceState(
        heater=data.heater,
        ventilation=data.ventilation,
        lighting=data.lighting,
        door=data.door,
        feeder=data.feeder
    )
    created_device_state = await DeviceStateRepository.create(new_device_state, db)
    await db.commit()
    await db.refresh(created_device_state)
    return DeviceResponse(status="ok")


async def device_state_get_service(db: AsyncSession):
    last_device_state = await DeviceStateRepository.get_last(db)
    if last_device_state is None:
        raise HTTPException(status_code=404, detail="Not found")

    return last_device_state