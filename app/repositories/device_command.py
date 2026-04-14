from app.repositories.base import BaseRepository
from app.models.device_command import DeviceCommand


class DeviceCommandRepository(BaseRepository):
    model = DeviceCommand
