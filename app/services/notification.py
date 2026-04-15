from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta

from app.repositories.event_log import EventLogRepository
from app.repositories.user import UserRepository
from app.schemas.notification import NotificationSettingsResponse, NotificationSettingsUpdateRequest,  \
    NotificationHistoryEvent


async def get_notification_settings_service(user_id: int, db: AsyncSession):
    user = await UserRepository.get_by_id(user_id, db)
    return NotificationSettingsResponse(
        alarm_temp_high=user.notif_alarm_temp_high,
        alarm_temp_low=user.notif_alarm_temp_low,
        alarm_humidity=user.notif_alarm_humidity,
        door_state=user.notif_door_state,
        device_offline=user.notif_device_offline,
    )


async def notification_settings_update_service(
        data: NotificationSettingsUpdateRequest ,
        user_id: int,
        db: AsyncSession
):
    user = await UserRepository.get_by_id(user_id, db)

    if data.alarm_temp_high is not None:
        user.notif_alarm_temp_high = data.alarm_temp_high
    if data.alarm_temp_low is not None:
        user.notif_alarm_temp_low = data.alarm_temp_low
    if data.alarm_humidity is not None:
        user.notif_alarm_humidity = data.alarm_humidity
    if data.door_state is not None:
        user.notif_door_state = data.door_state
    if data.device_offline is not None:
        user.notif_device_offline =  data.device_offline
    await db.commit()
    await db.refresh(user)

    return NotificationSettingsResponse(
        alarm_temp_high=user.notif_alarm_temp_high,
        alarm_temp_low=user.notif_alarm_temp_low,
        alarm_humidity=user.notif_alarm_humidity,
        door_state=user.notif_door_state,
        device_offline=user.notif_device_offline,
    )


async def get_notification_history_service(
        limit: int,
        offset: int,
        db: AsyncSession
):
    now = datetime.now(timezone.utc)
    period_start = now - timedelta(days=7)

    data = await EventLogRepository.filter_for_history(period_start, limit, offset, db)

    count = await EventLogRepository.count_for_history(period_start, db)

    return NotificationHistoryEvent(events=data, count=count)