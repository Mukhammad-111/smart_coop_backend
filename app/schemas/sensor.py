import datetime

from pydantic import BaseModel, Field


class SensorDataRequest(BaseModel):
    temperature: float | None = Field(None, ge=-40.0, le=85.0)
    humidity: float | None = Field(None, ge=0.0, le=100.0)
    light_level: int | None = Field(None, ge=0, le=65535)


class SensorDataResponse(BaseModel):
    status: str
    recorded_at: datetime.datetime