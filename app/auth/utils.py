import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status
from starlette.requests import Request

from app.core.config import settings
from app.core.database import get_db
from app.cruds import user_crud
from app.models.user_models import User
from app.services.hash_service import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


async def authenticate_user(username: str, password: str, db: AsyncSession):
    query = select(User).filter(User.name == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def get_current_user_payload(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            key=settings.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials, {error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def validate_token_type(
        payload: dict,
        token_type: str
):
    current_token_type = payload.get("token_type")
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token type {current_token_type!r} expected {token_type!r}',
        )


def get_current_user_from_token_of_type(token_type: str):
    async def get_current_user_form_token(
            payload: dict = Depends(get_current_user_payload),
            db: AsyncSession = Depends(get_db),
    ):
        await validate_token_type(payload=payload, token_type=token_type)
        user_id = payload.get("user_id")
        user = await user_crud.get_user(user_id=user_id, db=db)
        return user
    return get_current_user_form_token


get_current_user = get_current_user_from_token_of_type(token_type=settings.ACCESS_TOKEN_TYPE)


async def get_current_user_for_refresh(request: Request, db: AsyncSession = Depends(get_db)):
    refresh = request.cookies["refresh"] = str(request.cookies["refresh_token"])
    payload = await get_current_user_payload(token=refresh)
    await validate_token_type(payload=payload, token_type=settings.REFRESH_TOKEN_TYPE)
    user = await user_crud.get_user(user_id=payload["user_id"], db=db)
    return user