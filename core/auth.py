from fastapi import Depends, HTTPException, status, Query, HTTPException, Cookie, status, Header
from datetime import datetime, timedelta
import hashlib
import hmac
import os
from aiogram.exceptions import TelegramBadRequest
from urllib.parse import parse_qsl
from operator import itemgetter
from typing import Any,Dict
from sqlalchemy.ext.asyncio import AsyncSession
import json
from models.models import User
from sqlalchemy import select, insert, update, delete
from db.session import get_db



TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")
MAX_AUTH_AGE_SECONDS = int(os.getenv("MaxAuth", "7200"))
CHANNEL_ID = int(os.getenv("Channel"))


def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Проверяет корректность подписи Telegram WebApp (init_data).
    Возвращает True, если подпись совпадает, иначе False.
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        # Init data невалиден
        return False

    if "hash" not in parsed_data:
        return False

    hash_from_client = parsed_data.pop("hash")
    
    data_check_string = "\n".join(
        f"{k}={v}"
        for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=token.encode(),
        digestmod=hashlib.sha256
    )
    
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, hash_from_client)









async def current_user(
    session_id: str = Header(None, alias="X-Session-Id"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не передан session_id (неавторизован)"
        )

    
    result = await db.execute(
        select(User).where(User.session_id == session_id)
    )
    user = result.scalars().first()
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия не найдена"
        )

    
    if not user.session_created_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректная сессия"
        )

    now = datetime.utcnow()
    if now - user.session_created_at > timedelta(minutes=30):
        user.session_id = None
        user.session_created_at = None
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Сессия истекла, авторизуйтесь заново"
        )

    
    return {"telegram_id": user.tg_id}






