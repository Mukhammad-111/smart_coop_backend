from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DeviceCommand
from app.models.device_command import CommandType
from app.models.system_mode import ChangeSource
from app.repositories.device_command import DeviceCommandRepository
from app.repositories.system_mode import SystemModeRepository
from app.schemas.command import CommandStatusResponse, CommandAutoRequest, PendingCommandsResponse
from app.services.threshold_service import get_current_thresholds


async def command_executed_service(command_id: int, db: AsyncSession):
    command = await DeviceCommandRepository.get_by_id(command_id, db)
    if command is None:
        raise HTTPException(status_code=404, detail="Command Not found")

    command.is_executed = True
    command.executed_at = datetime.now(timezone.utc)
    await db.commit()
    return CommandStatusResponse(status="ok")


async def command_auto_service(data: CommandAutoRequest, db: AsyncSession):
    command = DeviceCommand(
        command_type=CommandType.set_auto,
        payload={"is_auto": data.is_auto}
    )
    await DeviceCommandRepository.create(command, db)

    last_mode = await SystemModeRepository.get_last(db)
    if last_mode is None:
        raise HTTPException(status_code=404, detail="Mode not found")

    last_mode.is_auto = data.is_auto
    last_mode.changed_by = ChangeSource.user

    await db.commit()

    return CommandStatusResponse(status="command_queued")


async def command_pending_get_service(db: AsyncSession):
    commands = await DeviceCommandRepository.get_pending(db)

    thresholds = await get_current_thresholds(db)

    schedule = await FeedScheduleRepository.get_active(db)

    return PendingCommandsResponse(
        commands=commands,
        thresholds=thresholds,
        feed_schedule=schedule
    )