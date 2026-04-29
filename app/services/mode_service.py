from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SystemMode, DeviceCommand, EventLog
from app.models.device_command import CommandType
from app.models.event_log import EventType, Severity
from app.models.system_mode import ChangeSource
from app.repositories.device_command import DeviceCommandRepository
from app.repositories.event_log import EventLogRepository
from app.repositories.system_mode import SystemModeRepository
from app.schemas.mode import ModeCurrentRequest, ModeCurrentResponse, ModeResponse, SetModeRequest


async def mode_current_create_service(data: ModeCurrentRequest,
                                      db: AsyncSession):
    last_mode = await SystemModeRepository.get_last(db)

    if last_mode and not last_mode.is_auto:
        return ModeCurrentResponse(status="ignored_manual_mode")

    new_system_mode = SystemMode(
        mode_name=data.mode_name,
        is_auto=data.is_auto,
        changed_by=ChangeSource.system
    )

    created_system_mode = await SystemModeRepository.create(new_system_mode, db)
    await db.commit()
    await db.refresh(created_system_mode)
    return ModeCurrentResponse(status="ok")


async def mode_current_get_service(db: AsyncSession):
    last_mode = await SystemModeRepository.get_last(db)
    if last_mode is None:
        raise HTTPException(status_code=404, detail="Mode not found")

    return last_mode


async def mode_set_service(data: SetModeRequest, db: AsyncSession):
    new_mode = SystemMode(
        mode_name=data.mode_name,
        is_auto=data.is_auto,
        changed_by=ChangeSource.user,
    )

    created_mode = await SystemModeRepository.create(new_mode, db)

    await DeviceCommandRepository.create(
            DeviceCommand(command_type=CommandType.set_mode,
            payload={"mode_name": data.mode_name.value}), db
    )
    if not data.is_auto:
        await DeviceCommandRepository.create(
            DeviceCommand(
            command_type=CommandType.set_auto,
            payload={"is_auto": False}
        ), db
    )

    event_log = EventLog(
        event_type=EventType.mode_change,
        severity=Severity.info,
        message="Mode set"
    )
    await EventLogRepository.create(event_log, db)

    await db.commit()
    await db.refresh(created_mode)
    return created_mode