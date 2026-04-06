from app.models import SensorReading
from app.repositories.base import BaseRepository


class SensorRepository(BaseRepository):
    model = SensorReading