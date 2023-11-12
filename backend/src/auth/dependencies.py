from fastapi import Depends, HTTPException, status, Request
from datetime import datetime
from jose import jwt, JWTError

from src.auth.dao import UsersDAO
from src.auth.schemas import TokenPayload, SystemUser
from src.auth.utils import ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY


async def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    print(token)
    if not token:
        print("Error 1")
        raise HTTPException(status_code=401)
    return token

async def get_current_user(token: str = Depends(get_refresh_token)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401)
    
    expire: str = payload.get("exp")
    
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=401)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    user = await UsersDAO.find_one_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401)
    
    user = user[0]
    return user


