from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1)
    phone: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe",
                "phone": "+919876543210"
            }
        }
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    }

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone: Optional[str] = None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
