from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.auth.utils import authenticate_user
from app.core.database import get_db
from app.schemas.token_schema import Token
from app.services.jwt_service import create_access_token, create_refresh_token


router = APIRouter(
    prefix='/login',
    tags=['login'],
)


@router.post("/")
async def login_for_access_token(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        'sub': user.name,
        'user_id': user.id,
    }
    access_token = await create_access_token(payload=data)
    refresh_token = await create_refresh_token(payload=data, response=response)
    return Token(refresh_token=refresh_token ,access_token=access_token)
