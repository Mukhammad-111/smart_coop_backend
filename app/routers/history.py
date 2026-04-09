from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_db, get_current_user
from app.models import User
from app.schemas.history import SensorHistoryResponse, PeriodValue, ParameterValue, HistoryDataResponse
from app.services.history import get_history_sensor_service, get_history_device_service, get_history_modes_service

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/sensor", response_model=SensorHistoryResponse)
async def history_sensor_get(period: PeriodValue = Query(default=PeriodValue.h24),
                             parameter: ParameterValue = Query(default=ParameterValue.all),
                             limit: int = Query(default=1000, ge=1, le=5000),
                             offset: int = Query(default=0, ge=0),
                             user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    return await get_history_sensor_service(period, parameter, limit, offset, db)


@router.get("/device", response_model=HistoryDataResponse)
async def history_device_get(period: PeriodValue = Query(default=PeriodValue.h24),
                             limit: int = Query(default=500, ge=1, le=2000),
                             offset: int = Query(default=0, ge=0),
                             user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    return await get_history_device_service(period, limit, offset, db)


@router.get("/modes", response_model=HistoryDataResponse)
async def history_modes_get(period: PeriodValue = Query(default=PeriodValue.h24),
                            limit: int = Query(default=100, ge=1),
                            offset: int = Query(default=0, ge=0),
                            user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    return await get_history_modes_service(period, limit, offset, db)