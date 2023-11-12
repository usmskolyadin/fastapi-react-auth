from datetime import datetime
from pydantic import BaseModel, EmailStr

class SUserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: str
    exp: datetime


class SystemUser(BaseModel):
    id: str
    username: str
    email: str
    registered_at: datetime
    
    class Config:
        orm_mode = True