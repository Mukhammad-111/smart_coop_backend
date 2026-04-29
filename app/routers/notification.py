from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_current_user, get_db
from app.models import User
from app.schemas.notification import NotificationSettingsResponse, NotificationHistoryResponse, \
    NotificationSettingsUpdateRequest
from app.services.notification import get_notification_settings_service, get_notification_history_service, \
    notification_settings_update_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/settings", response_model=NotificationSettingsResponse)
async def get_notification_settings(user: User = Depends(get_current_user),
                                    db: AsyncSession = Depends(get_db)):
    return await get_notification_settings_service(user.id, db)


@router.put("/settings", response_model=NotificationSettingsResponse)
async def update_notification_settings(
        data: NotificationSettingsUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return await notification_settings_update_service(data, user.id, db)


@router.get("/history", response_model=NotificationHistoryResponse)
async def get_notification_history(
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return await get_notification_history_service(limit, offset, db)