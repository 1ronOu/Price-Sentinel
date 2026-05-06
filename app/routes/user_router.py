from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user, get_current_user_for_refresh
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserOut
from app.cruds import user_crud
from app.models.user_models import User
from app.services.jwt_service import create_access_token

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix='/user',
    tags=['user'],
)

@router.post('/create', response_model=UserOut)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(user=user, db=db)


@router.get('/me', response_model=UserOut)
async def read_user(
        current_user: User = Depends(get_current_user)
):
    return current_user


@router.get('/get_all', response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db=db)


@router.post('/refresh')
async def refresh_jwt(
        user = Depends(get_current_user_for_refresh),
):
    payload = {
        'sub': user.name,
        'user_id': user.id,
    }
    new_access_token = await create_access_token(payload=payload)
    return {'access_token': new_access_token}
