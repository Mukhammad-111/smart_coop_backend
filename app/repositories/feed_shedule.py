from app.repositories.base import BaseRepository
from app.models.feed_schedule import FeedSchedule


class FeedScheduleRepository(BaseRepository):
    model = FeedSchedule