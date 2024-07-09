from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select, update, delete


async def set_user(tg_id: int)-> None:
    async with async_session() as session:
        user =  await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

async def add_item(data):
    item = Item( 
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=float(data['categories']),
        image=data['image']
    )
    async with async_session() as session:
     session.add(item)
     await session.commit()
        
async def get_items():
    async with async_session() as session:
        return await session.scalars(select(Item))

async def update_items(item_id: int, data):
    query = update(Item).where(Item.id == item_id).values(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=float(data['categories']),
        image=data['image']
    )
    async with async_session() as session:
        await session.execute(query)
        await session.commit()

async def delete_item(item_id: int):
    query = delete(Item).where(Item.id == item_id)
    async with async_session() as session:
       await session.execute(query)
       await session.commit()