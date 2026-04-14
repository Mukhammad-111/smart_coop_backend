from app.repositories.base import BaseRepository
from app.models.event_log import EventLog


class EventLogRepository(BaseRepository):
    model = EventLog