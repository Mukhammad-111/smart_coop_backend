import enum

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class EventItem(BaseModel):
    id: int
    event_type: str
    severity: str
    message: str
    value: float | None
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventsResponse(BaseModel):
    events: list[EventItem]
    count: int


class SeverityFilter(enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"
    all = "all"