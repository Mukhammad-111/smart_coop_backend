from app.models import Threshold
from app.repositories.base import BaseRepository


class ThresholdRepository(BaseRepository):
    model = Threshold