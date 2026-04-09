from app.models.event import Event
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository):
    model = Event