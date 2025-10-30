from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Item
from ..schemas import ItemIn, ItemOut

router = APIRouter(prefix="/items", tags=["items"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("", response_model=list[ItemOut])
async def list_items(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Item).order_by(Item.id.desc()))
    return res.scalars().all()

@router.post("", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemIn, db: AsyncSession = Depends(get_db)):
    item = Item(title=payload.title)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
