from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SensorReading, DeviceState
from app.models.device_state import DoorStatus
from app.repositories.device_state import DeviceStateRepository
from app.repositories.sensor_reading import SensorRepository
from app.repositories.thresholds import ThresholdRepository
from app.repositories.user import UserRepository
from app.schemas.sensor import SensorDataRequest, SensorDataResponse, CurrentSensorResponse
from app.services import push_service
from app.utils.sensor_status import get_temperature_status, get_humidity_status, get_light_status


async def sensor_data_service(data: SensorDataRequest, db: AsyncSession, user_id: int):
    new_sensor_data = SensorReading(
        temperature=data.temperature,
        humidity=data.humidity,
        light_level=data.light_level
    )
    created_sensor_data = await SensorRepository.create(new_sensor_data, db)

    threshold = await ThresholdRepository.get_active(db)
    if threshold is None:
        raise HTTPException(status_code=500, detail="Thresholds not configured")


    user = await UserRepository.get_by_id(user_id, db)

    await push_service.check_and_notify(data.temperature, data.humidity, threshold, user)

    device_state = await DeviceStateRepository.get_first(db)
    if not device_state:
        device_state = DeviceState(
        heater=False,
        ventilation=False,
        lighting=False,
        door=DoorStatus.closed,
        feeder=False,
        recorded_at=datetime.now(timezone.utc)
        )
        await DeviceStateRepository.create(device_state, db)
    else:
        device_state.recorded_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(device_state)

    return SensorDataResponse(
        status="ok",
        recorded_at=created_sensor_data.recorded_at
    )


async def sensor_current_service(user_id: int, db: AsyncSession):
    reading = await SensorRepository.get_last_reading(db)
    if reading is None:
        raise HTTPException(status_code=404, detail="No sensor data")

    threshold = await ThresholdRepository.get_active(db)
    if threshold is None:
        raise HTTPException(status_code=404, detail="Threshold not configured")

    return CurrentSensorResponse(
        temperature=reading.temperature,
        humidity=reading.humidity,
        light_level=reading.light_level,
        recorded_at=reading.recorded_at,
        temperature_status=get_temperature_status(reading.temperature, threshold),
        humidity_status=get_humidity_status(reading.humidity, threshold),
        light_status=get_light_status(reading.light_level, threshold)
    )