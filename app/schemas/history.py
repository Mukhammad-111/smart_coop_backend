import enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.mode import ModeResponse


class PeriodValue(enum.Enum):
    h24 = "24h"
    d7 = "7d"
    d30 = "30d"


class ParameterValue(enum.Enum):
    temperature = "temperature"
    humidity = "humidity"
    light_level = "light_level"
    all = "all"


class SensorDataItem(BaseModel):
    temperature: float | None
    humidity: float | None
    light_level: int | None
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SensorHistoryResponse(BaseModel):
    data: list[SensorDataItem]
    count: int
    period: str
    stats: dict


class DeviceStateItem(BaseModel):
    heater: bool
    ventilation: bool
    lighting: bool
    door: str
    feeder: bool
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoryDataResponse(BaseModel):
    data: list[ModeResponse]
    count: int