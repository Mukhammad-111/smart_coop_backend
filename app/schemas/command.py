from pydantic import BaseModel

from app.models.device_command import CommandType
from app.schemas.thresholds import ThresholdsResponse


class CommandStatusResponse(BaseModel):
    status: str


class CommandAutoRequest(BaseModel):
    is_auto: bool


class PendingCommandsResponse(BaseModel):
    commands: list[CommandItem]
    thresholds: ThresholdsResponse
    feed_schedule: list[] #TODO FeedSchelduleItem


class CommandItem(BaseModel):
    id: int
    command_type: CommandType
    payload: dict | None


class CommandDoorRequest(BaseModel):
    action: