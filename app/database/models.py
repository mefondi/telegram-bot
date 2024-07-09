import os
from sqlalchemy import BigInteger, String, ForeignKey, Float, DateTime,func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True)
    update: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column(Float(asdecimal=True))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    image: Mapped[str] = mapped_column(String(150))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
