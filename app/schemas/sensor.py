import datetime
import enum

from pydantic import BaseModel, Field


class SensorDataRequest(BaseModel):
    temperature: float | None = Field(None, ge=-40.0, le=85.0)
    humidity: float | None = Field(None, ge=0.0, le=100.0)
    light_level: int | None = Field(None, ge=0, le=65535)


class SensorDataResponse(BaseModel):
    status: str
    recorded_at: datetime.datetime


class TemperatureStatus(str, enum.Enum):
    normal = "normal"
    low = "low"
    high = "high"
    critical_low = "critical_low"
    critical_high = "critical_high"
    sensor_error = "sensor_error"


class HumidityStatus(str, enum.Enum):
    normal = "normal"
    high = "high"
    critical = "critical"
    sensor_error = "sensor_error"


class LightStatus(str, enum.Enum):
    dark = "dark"
    normal = "normal"
    bright = "bright"
    sensor_error = "sensor_error"


class CurrentSensorResponse(BaseModel):
    temperature: float | None
    humidity: float | None
    light_level: int | None
    recorded_at: datetime.datetime
    temperature_status: TemperatureStatus
    humidity_status: HumidityStatus
    light_status: LightStatus