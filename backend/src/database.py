from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_async_engine(settings.db.url, echo=True)
Base = declarative_base()
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)