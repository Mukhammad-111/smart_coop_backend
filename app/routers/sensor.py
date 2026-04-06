from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import verify_api_key
from app.dependencies.dependencies import get_db
from app.schemas.sensor import SensorDataResponse, SensorDataRequest
from app.services.sensor_service import sensor_data_service

router = APIRouter(prefix="sensor", tags=["Sensor"])


@router.post("/data", response_model=SensorDataResponse)
async def sensor_data(data: SensorDataRequest,
               db: AsyncSession = Depends(get_db),
               _: None = Depends(verify_api_key)):
    return await sensor_data_service(data, db)