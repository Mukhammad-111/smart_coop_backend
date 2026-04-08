from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SystemMode
from app.models.system_mode import ChangeSource
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
    return last_mode


async def mode_set_service(data: SetModeRequest, db: AsyncSession):
    last_mode = await SystemModeRepository.get_last(db)
    system_mode = await SystemModeRepository.update(last_mode, data, db)
    system_mode.changed_by =  ChangeSource.user
    await db.commit()
    return system_mode