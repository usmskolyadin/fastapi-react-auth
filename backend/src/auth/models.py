from datetime import datetime
from sqlalchemy import Column, JSON, ForeignKey, String, Table, TIMESTAMP, MetaData, Integer

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
)

tokens = Table(
    "tokens",
    metadata,
    Column("user", Integer, ForeignKey('users.id')),
    Column("refresh_token", String, nullable=False),
)

'''
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
'''