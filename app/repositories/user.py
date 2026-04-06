from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def get_by_email(cls, email: str, db: AsyncSession):
        result = await db.execute(select(cls.model).where(cls.model.email == email))
        return result.scalar_one_or_none()