from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationSettingsResponse(BaseModel):
    alarm_temp_high: bool
    alarm_temp_low: bool
    alarm_humidity: bool
    door_state: bool
    device_offline: bool

    model_config = ConfigDict(from_attributes=True)


class NotificationSettingsUpdateRequest(BaseModel):
    alarm_temp_high: bool | None
    alarm_temp_low: bool | None
    alarm_humidity: bool | None
    door_state: bool | None
    device_offline: bool | None


class HistoryEventItem(BaseModel):
    id: int
    event_type: str
    severity: str
    message: str
    value: float | None
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationHistoryEvent(BaseModel):
    events: list[HistoryEventItem]
    count: int