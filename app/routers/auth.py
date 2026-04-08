from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.dependencies.dependencies import get_db, get_current_user
from app.models import User
from app.schemas.auth import (RegisterRequest, UserResponse, TokenResponse, LoginRequest,
                              RefreshResponse, RefreshRequest, MessageResponse, LogoutRequest,
                              PushTokenRequest, PushTokenDeleteRequest, UserMeResponse)
from app.services.auth_service import (register_service, login_service, refresh_service,
                                       logout_service, me_service, push_token_service,
                                       push_token_delete_service)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest,
                   db: AsyncSession = Depends(get_db)):
    return await register_service(data, db)


@router.post("/login",
             response_model=TokenResponse)
async def login(data: LoginRequest,
                db: AsyncSession = Depends(get_db)):
    return await login_service(data, db)


@router.post("/refresh",
             response_model=RefreshResponse)
async def refresh(token_data: RefreshRequest,
                  db: AsyncSession = Depends(get_db)):
    return await refresh_service(token_data, db)


@router.post("/logout", response_model=MessageResponse)
async def logout(data: LogoutRequest,
                 current_user: User = Depends(get_current_user),
                 db: AsyncSession = Depends(get_db)):
    return await logout_service(current_user, db, data.token)


@router.get("/me", response_model=UserMeResponse)
async def me(current_user: User = Depends(get_current_user),
             db: AsyncSession = Depends(get_db)):
    return await me_service(current_user, db)


@router.post("push-token", response_model=MessageResponse)
async def push_token(data: PushTokenRequest,
                     current_user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    return await push_token_service(current_user, data, db)

@router.delete("push-token", response_model=MessageResponse)
async def push_token_delete(data: PushTokenDeleteRequest,
                            current_user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    return await push_token_delete_service(current_user, data.token, db)