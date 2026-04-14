from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.feed_shedule import (
    FeedScheduleItem,
    FeedScheduleCreateRequest,
    FeedScheduleUpdateRequest,
    FeedTriggerRequest,
    FeedTriggerResponse
)
from app.services.feed_schedule_service import (
    get_feed_schedules as get_feed_schedules_service,
    create_feed_schedule as create_feed_schedule_service,
    update_feed_schedule as update_feed_schedule_service,
    delete_feed_schedule as delete_feed_schedule_service,
    trigger_feed as trigger_feed_service, get_feed_schedules
)

router = APIRouter(prefix="/feed", tags=["Feed Schedule"])


@router.get("/schedule", response_model=list[FeedScheduleItem])
async def get_feed_schedule(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_feed_schedules(db)


@router.post("/schedule", response_model=FeedScheduleItem, status_code=status.HTTP_201_CREATED)
async def create_feed_schedule(
    data: FeedScheduleCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await create_feed_schedule_service(data, db)


@router.put("/schedule/{id}", response_model=FeedScheduleItem)
async def update_feed_schedule(
    data: FeedScheduleUpdateRequest,
    id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await update_feed_schedule_service(id, data, db)


@router.delete("/schedule/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feed_schedule(
    id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await delete_feed_schedule_service(id, db)


@router.post("/trigger", response_model=FeedTriggerResponse)
async def trigger_feed(
    data: FeedTriggerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await trigger_feed_service(data, current_user.id, db)
