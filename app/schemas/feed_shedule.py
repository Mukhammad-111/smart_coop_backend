from pydantic import BaseModel, Field, ConfigDict
import datetime


class FeedScheduleItem(BaseModel):
    id: int
    feed_time: datetime.time
    duration_seconds: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FeedScheduleCreateRequest(BaseModel):
    feed_time: datetime.time = Field(..., description="Время кормления в формате HH:MM:SS (UTC)")
    duration_seconds: int = Field(..., ge=1, le=60, description="Длительность работы мотора в секундах")
    is_active: bool = Field(default=True, description="Активно ли время кормления")


class FeedScheduleUpdateRequest(BaseModel):
    feed_time: datetime.time = Field(..., description="Время кормления в формате HH:MM:SS (UTC)")
    duration_seconds: int = Field(..., ge=1, le=60, description="Длительность работы мотора в секундах")
    is_active: bool = Field(..., description="Активно ли время кормления")


class FeedTriggerRequest(BaseModel):
    duration_seconds: int = Field(..., ge=1, le=60, description="Длительность кормления в секундах")


class FeedTriggerResponse(BaseModel):
    status: str
    command_id: int
