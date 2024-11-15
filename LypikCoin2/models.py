from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    coin: Mapped[int] = mapped_column()
    time_exit: Mapped[int] = mapped_column()
    energy: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
        
async def asyns_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
