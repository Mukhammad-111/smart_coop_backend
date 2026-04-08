from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import verify_api_key, get_current_user
from app.dependencies.dependencies import get_db
from app.models import User
from app.schemas.sensor import SensorDataResponse, SensorDataRequest, CurrentSensorResponse
from app.services.sensor_service import sensor_data_service, sensor_current_service

router = APIRouter(prefix="/sensor", tags=["Sensor"])


@router.post("/data", response_model=SensorDataResponse)
async def sensor_data(data: SensorDataRequest,
               db: AsyncSession = Depends(get_db),
               user: User = Depends(verify_api_key)):
    return await sensor_data_service(data, db, user.id)


@router.get("/current", response_model=CurrentSensorResponse)
async def sensor_current(user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    return await sensor_current_service(user.id, db)