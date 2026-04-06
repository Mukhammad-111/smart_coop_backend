from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.refresh_token import RefreshToken


class RefreshTokenRepository(BaseRepository):
    model = RefreshToken

    @classmethod
    async def create_token(
            cls,
            user_id: int,
            token: str,
            db: AsyncSession):
        new_token = cls.model(user_id=user_id, token=token)

        db.add(new_token)
        await db.flush()
        return new_token


    @classmethod
    async def get_by_refresh_token(
            cls,
            refresh_token: str,
            db: AsyncSession):
        result = await db.execute(select(cls.model).where(cls.model.token == refresh_token))
        return result.scalar_one_or_none()

    @classmethod
    async def delete_token(
            cls,
            user_id: int,
            db: AsyncSession):
        await db.execute(delete(cls.model).where(cls.model.user_id ==user_id))