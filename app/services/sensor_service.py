from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SensorReading
from app.repositories.sensor_reading import SensorRepository
from app.repositories.thresholds import ThresholdRepository
from app.repositories.user import UserRepository
from app.schemas.sensor import SensorDataRequest
from app.services import push_service


async def sensor_data_service(data: SensorDataRequest, db: AsyncSession):
    new_sensor_data = SensorReading(
        temperature=data.temperature,
        humidity=data.humidity,
        light_level=data.light_level
    )
    created_sensor_data = await SensorRepository.create(new_sensor_data, db)

    threshold = await ThresholdRepository.get_by_id(1, db)
    if not threshold:
        raise HTTPException(status_code=500, detail="Thresholds not configured")

    user = await UserRepository.get_by_id(1, db)

    await push_service.check_and_notify(data.temperature, data.humidity, threshold, user)

    return {"status": "ok",
            "recorded_at": created_sensor_data.recorded_at}