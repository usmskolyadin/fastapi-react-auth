import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from src.auth.dao import UsersDAO
from src.config import settings
from pydantic import EmailStr
from fastapi import HTTPException

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = (60 * 24 * 7) * 2 # 14 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.auth.JWT_SECRET_KEY   # should be kept secret
JWT_REFRESH_SECRET_KEY = settings.auth.JWT_REFRESH_SECRET_KEY   # should be kept secret


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})
    
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        ALGORITHM
        )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})
    
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_REFRESH_SECRET_KEY,
        ALGORITHM
        )
    return encoded_jwt

    
async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    
    return user
