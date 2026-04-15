from fastapi import Depends, HTTPException, Header, Query
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import decode_access_token
from app.database.session import async_session_local
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.repositories.user import UserRepository


async def get_db():
    async with async_session_local() as session:
        yield session


security = HTTPBearer()

security_optional = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token=token)
        user_id: int | None = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserRepository.get_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_user_optional(
        token: str | None = Query(None),
        credentials: HTTPAuthorizationCredentials | None = Depends(security_optional),
        db: AsyncSession = Depends(get_db)
):
    jwt_token = None

    if token:
        jwt_token = token
    elif credentials:
        jwt_token = credentials.credentials

    if not jwt_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(jwt_token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserRepository.get_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key"),
                         db: AsyncSession = Depends(get_db)):
    user = await UserRepository.get_by_api_key(x_api_key, db)

    if not user or not user.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user