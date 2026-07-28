from fastapi import Depends
from typing import Optional
from app.model import User
from pydantic import BaseModel


class RegisterUser(BaseModel):
    full_name: str
    email: str
    phone_no: int
    password: str
    role: Optional[str] = "user"
    
    
class LoginUser(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_no: int
    role: str

    class Config:
        from_attributes = True
    
class RegisterAdmin(BaseModel):
    full_name: str
    email: str
    phone_no: int
    password: str
    role: Optional[str] = "admin"
    
class LoginAdmin(BaseModel):
    email: str
    password: str
    
class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_no: int
    role: str

    class Config:
        from_attributes = True
