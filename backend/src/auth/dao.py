from src.dao import SQLAlchemyRepository
from src.auth.models import users, tokens
from sqlalchemy import insert, select, update, delete, desc
from src.database import async_session_maker


class UsersDAO(SQLAlchemyRepository):
    model = users
    
    @classmethod
    async def get_all(cls) -> list:
        async with async_session_maker() as session:
            query = select(
                cls.model.c.id,
                cls.model.c.username,
                cls.model.c.email,
                cls.model.c.registered_at
            )
            result = await session.execute(query)
            return result.fetchall()        
    
    @classmethod
    async def get_all_with_filters(cls, **filters) -> list:
        async with async_session_maker() as session:
            query = select(
                cls.model.c.id,
                cls.model.c.username,
                cls.model.c.email,
                cls.model.c.registered_at
            ).filter_by(
                **filters
            )
            result = await session.execute(query)
            return result.fetchall()
    
    @classmethod
    async def find_one_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(
                cls.model.c.id,
                cls.model.c.username,
                cls.model.c.email,
                cls.model.c.registered_at
            ).filter_by(id=id)
            
            result = await session.execute(query)
            return result.fetchall()
