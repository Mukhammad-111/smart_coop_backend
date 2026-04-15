from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_current_user, get_db
from app.models import User
from app.schemas.system import SystemStatusResponse
from app.services.system_service import system_health_service, system_status_service

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/health")
async def get_system_health(db: AsyncSession = Depends(get_db)):
    return await system_health_service(db)


@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status(user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    return await system_status_service(user.id, db)