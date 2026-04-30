from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserOut
from app.cruds import user_crud

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/create', response_model=UserOut)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(user=user, db=db)


@router.get('/get')
async def read_user(
    user_name: str,
    db: AsyncSession = Depends(get_db)
):
    return await user_crud.get_user_by_user_name(user_name=user_name, db=db)


@router.get('/get_all')
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db=db)
