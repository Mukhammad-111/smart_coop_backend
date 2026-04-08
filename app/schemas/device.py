import datetime

from pydantic import BaseModel, ConfigDict

from app.models.device_state import DoorStatus


class DeviceStateRequest(BaseModel):
    heater: bool
    ventilation: bool
    lighting: bool
    door: DoorStatus
    feeder: bool


class DeviceResponse(BaseModel):
    status: str


class DeviceStateResponse(BaseModel):
    heater: bool
    ventilation: bool
    lighting: bool
    door: DoorStatus
    feeder: bool
    recorded_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)