from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.items import ItemOut, ItemCreate
from app import crud

router = APIRouter(
    prefix='/item',
    tags=['items']
)

@router.post('/create', response_model=ItemOut)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_item(item=item, db=db)


@router.get('/get_multiple_items')
async def get_multiple_items(db: AsyncSession = Depends(get_db)):
    items = await crud.get_multiple_items(db=db)
    return items

@router.get('/read_all', response_model=list[ItemOut])
async def read_all_items(db: AsyncSession = Depends(get_db)):
    return await crud.read_items(db=db)


@router.delete('/delete_item/{item_id}')
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_item(item_id=item_id, db=db)