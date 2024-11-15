from models import async_session
from models import User
from sqlalchemy import select, update #, delete, desc
from sqlalchemy.future import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name="None", coin=0, energy=1000, time_exit=0))
            await session.commit()

# МОНЕТЫ
async def update_coin(coin, tg_id):
    async with async_session() as session:
        # Получаем пользователя по tg_id
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            user.coin = coin  # Изменяем поле coin
            await session.commit()  # Сохраняем изменения
            
        else:
            pass
# 1423388201
async def get_coin(tg_id):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
      
        if user:
            return user.coin
        else:
            pass
        await session.commit()

# ВРЕМЯ ВЫХОДА
async def update_time(time_exit, tg_id):
    async with async_session() as session:
        # Получаем пользователя по tg_id
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            user.time_exit = time_exit  # Изменяем поле coin
            await session.commit()  # Сохраняем изменения
        else:
            pass  

async def get_time(tg_id):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            return user.time_exit
        else:
            pass
        await session.commit()     

# ЭНЕРГИЯ
async def get_energy(tg_id):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            return user.energy
        else:
            pass
        await session.commit()
        
async def update_energy(tg_id):
    async with async_session() as session:
        # Получаем пользователя по tg_id
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            user.energy -=1  # Изменяем поле coin
            await session.commit()  # Сохраняем изменения
        else:
            pass 

async def update_energy_plus(tg_id):
    async with async_session() as session:
        # Получаем пользователя по tg_id
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            user.energy +=1  # Изменяем поле coin
            await session.commit()  # Сохраняем изменения
            
        else:
            pass 
            
async def get_id(tg_id):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            return True
        else:         
            pass
        await session.commit()

async def update_name(tg_id, name):
    async with async_session() as session:
        # Получаем пользователя по tg_id
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
        
        if user:
            user.name = name  # Изменяем поле coin
            await session.commit()  # Сохраняем изменения
        else:
            pass

async def get_stat(i):
    async with async_session() as session:
        Statind = []
        for x in range(1, i):
            try:
                stmt = select(User).where(User.id == x)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()  # Получаем единственного пользователя или None
                
                if user:
                    Statind.append([user.coin, user.name, user.time_exit])
                else:         
                    pass
                await session.commit()
                if x == i-1:
                    return Statind
            except: pass
            
