from datetime import timedelta, datetime, timezone

import jwt
from starlette.responses import Response

from app.core.config import settings


async def create_jwt(
        token_type: str,
        payload: dict,
        expires_delta: timedelta,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
):
    payload['token_type'] = token_type
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt


async def create_access_token(
        payload: dict,
        token_type: str = settings.ACCESS_TOKEN_TYPE,
        expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
):
    token = await create_jwt(
        token_type=token_type,
        payload=payload,
        expires_delta=expires_delta,
    )
    return token


async def create_refresh_token(
        response: Response,
        payload: dict,
        token_type: str = settings.REFRESH_TOKEN_TYPE,
        expires_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
):
    token = await create_jwt(
        token_type=token_type,
        payload=payload,
        expires_delta=expires_delta,
    )
    response.set_cookie(
        key='refresh_token',
        value=token,
        httponly=True,
        secure=True,
        samesite='lax',
        path='/user/refresh',
    )
    return token