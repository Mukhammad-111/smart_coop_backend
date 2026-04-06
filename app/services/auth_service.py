from datetime import datetime

from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import hash_password, verify_password, create_access_token, create_refresh_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token
from app.models.user import User
from app.repositories.push_token import PushTokenRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, PushTokenRequest


async def register_service(data: RegisterRequest, db: AsyncSession):
    existing_user = await UserRepository.get_by_email(data.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = hash_password(data.password)

    new_user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=password_hash
    )
    created_user = await UserRepository.create(new_user, db)
    await db.commit()
    await db.refresh(created_user)
    return created_user


async def login_service(data: LoginRequest, db: AsyncSession):
    user = await UserRepository.get_by_email(data.email, db)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))
    refresh_db = await RefreshTokenRepository.create_token(user.id, refresh_token, db)
    await db.commit()
    await db.refresh(refresh_db)
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}


async def refresh_service(token_data: RefreshRequest, db: AsyncSession):
    refresh_t = token_data.refresh_token
    try:
        payload = decode_access_token(refresh_t)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    except (JWTError, Exception):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    token_obj = await RefreshTokenRepository.get_by_refresh_token(refresh_t, db)
    if not token_obj or token_obj.is_revoked:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = str(payload["sub"])
    access_token = create_access_token({"sub": user_id})
    return {"access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}


async def logout_service(current_user: User,
                         db: AsyncSession,
                         push_token: str | None = None):
    await RefreshTokenRepository.delete_token(current_user.id, db)

    if push_token:
        token_obj = await PushTokenRepository.get_token(push_token, db)
        if token_obj:
            token_obj.is_active = False
            db.add(token_obj)

    await db.commit()
    return {"message": "Logout successful"}

async def me_service(current_user: User, db: AsyncSession):
    user = await UserRepository.get_by_id(current_user.id, db)
    return user


async def push_token_service(current_user: User,
                             data: PushTokenRequest,
                             db: AsyncSession):
    token = await PushTokenRepository.get_token(data.token, db)
    if token:
        token.updated_at = datetime.utcnow()
        token.is_active = True
        token.user_id = current_user.id
        await db.commit()
        return {"message": "Push token registered"}

    created_token = await PushTokenRepository.create_token(
        user_id=current_user.id,
        token=data.token,
        platform=data.platform,
        db=db)
    await db.commit()
    await db.refresh(created_token)
    return {"message": "Push token registered"}


async def push_token_delete_service(current_user: User,
                                    token: str,
                                    db: AsyncSession):
    push_token = await PushTokenRepository.get_token(token=token, db=db)
    if push_token.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if push_token:
        push_token.is_active = False
        await db.commit()
    return {"message": "Push token removed"}