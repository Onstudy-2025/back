from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from fastapi.exceptions import HTTPException
import os 
from typing import Any, List
from uuid import UUID
from core.auth import check_webapp_signature
from schemas.schemas import UserCheck
import aiohttp
import asyncio
import uuid
from urllib.parse import parse_qsl
from models.models import User
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime 
import time 
from schemas.schemas import AuthInitRequest, AuthInitResponse
from sqlalchemy import select, insert, update, delete
from db.session import get_db
from core.auth import TELEGRAM_BOT_TOKEN
import json 

router = APIRouter()






@router.post(
    "/auth/init/",
    response_model=AuthInitResponse,        
    summary="Авторизация + проверка наличия в канале"
)
async def auth_init(
    request: AuthInitRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> AuthInitResponse:
    # 1. Парсим init_data в словарь
    init_data = request.init_data
    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невалидный формат init_data"
        )

    # 2. Проверяем подпись WebApp
    if not check_webapp_signature(TELEGRAM_BOT_TOKEN, init_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid WebApp signature"
        )

    # 3. Проверяем auth_date
    auth_date_str = parsed.get("auth_date")
    if auth_date_str is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="auth_date отсутствует в init_data"
        )
    try:
        auth_date = int(auth_date_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный auth_date"
        )
    if int(time.time()) - auth_date > 2 * 3600:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="InitData устарели (больше 2 часов)"
        )

    # 4. Извлекаем user.id из вложенного JSON
    user_json = parsed.get("user")
    if not user_json:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В init_data нет поля user"
        )
    try:
        user_data = json.loads(user_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невалидный JSON в поле user"
        )
    user_id = user_data.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В поле user нет id"
        )
    try:
        telegram_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный Telegram ID"
        )

    # 5. Ищем или создаём пользователя в базе
    result = await db.execute(select(User).where(User.tg_id == telegram_id))
    user = result.scalars().first()
    if not user:
        user = User(
            tg_id=telegram_id,
            sub_type=None,
            last_payment=None,
            expired_date=None,
            session_id=None,
            session_created_at=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # 6. Генерируем новую сессию и сохраняем
    new_session_id = str(uuid.uuid4())
    user.session_id = new_session_id
    user.session_created_at = datetime.utcnow()
    await db.commit()

    


    

    # 8. Проверяем, состоит ли пользователь в канале
    is_member = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://onstudyithack2025.ru/user_in_channel",
                json={"user_id": telegram_id}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    is_member = bool(data.get("is_member", False))
    except Exception:
        is_member = False

    # 9. Возвращаем ответ
    return AuthInitResponse(
        status="ok",
        message="Авторизация успешна",
        is_member=is_member,
        session_id=new_session_id
    )











@router.get("/me")
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    result = await db.execute(select(User).where(User.session_id == session_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return {
        "id": user.tg_id,
        "sub_type": user.sub_type
    }
