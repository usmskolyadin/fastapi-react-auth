from fastapi import APIRouter, HTTPException, Response, Depends
from src.auth.dao import UsersDAO
from src.auth.utils import authenticate_user, create_access_token, create_refresh_token, get_hashed_password, verify_password
from src.auth.schemas import SUserAuth, SystemUser
from src.auth.dependencies import get_current_user


auth = APIRouter(
    tags=["Auth & Users"]
)


@auth.post('/register', summary="Create new user")
async def register(user: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=403)
    hashed_password = get_hashed_password(user.password)
    
    user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    await UsersDAO.add_one(user)
    

@auth.post('/login', summary="Signin")
async def login(user: SUserAuth, response: Response):
    user = await authenticate_user(email=user.email, password=user.password)
    if not user:
        raise HTTPException(status_code=401)

    access_token = create_access_token({"sub":  str(user.id)})
    refresh_token = create_refresh_token({"sub":  str(user.id)})

    response.set_cookie("refresh_token", refresh_token, httponly=True)
        
    return {
        "id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    

@auth.post('/refresh')
async def refresh(user: SystemUser = Depends(get_current_user)) -> dict:
    if not user:
        HTTPException(status_code=401, detail="refresh token is not valid")
        
    access_token = create_access_token({"sub":  str(user.id)})
    refresh_token = create_refresh_token({"sub":  str(user.id)})
            
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    
@auth.post('/logout')
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"user": "successfully logout"}
    

@auth.get('/users')
async def find_all_users(q: dict) -> list:
    return await UsersDAO.get_all_with_filters(**q)


@auth.get('/users/me', summary='Get details of currently logged in user')
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user


