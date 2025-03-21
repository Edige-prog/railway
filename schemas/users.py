from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    fullname: str
    password: str
    photo_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "lily.potter@hogwarts.com",
                "fullname": "Lily Potter",
                "password": "BestMagician",
            }
        }


class UserInfo(BaseModel):
    id:int
    email: EmailStr
    fullname: str
    password_hashed: str
    photo_url: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    new_password: Optional[str] = None
    email: Optional[EmailStr] = None
