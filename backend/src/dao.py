from abc import ABC

from sqlalchemy import insert, select, update, delete, desc
from src.database import async_session_maker

class AbstractRepository(ABC):
    pass


class SQLAlchemyRepository(AbstractRepository):
    model = None
    
    @classmethod
    async def add_one(cls, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()
            return stmt

    @classmethod
    async def edit_one(cls, id: int, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(id=id).returning(cls.model.id)
            res = await session.execute(stmt)
            return res.scalar_one()
    
    @classmethod    
    async def edit_by_filter(cls, filters: dict, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(**filters).returning(cls.model.id)
            res = await session.execute(stmt)
            return res.scalar_one()
    
    @classmethod
    async def find_one_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.first()
    
    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(**filter_by)
            res = await session.execute(stmt)
            return res
    
    @classmethod
    async def find_all(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars.all()        
    

    async def get_attrs_with_filters(self, *attrs, **filter_by) -> list:
        stmt = select(*attrs).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res
    
    async def get_last(self):
        stmt = select(self.model).order_by(desc(self.model.c.date)).limit(1)
        res = await self.session.execute(stmt)
        res = res.scalar_one().get_schema()
        return res

    async def get_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res
    
