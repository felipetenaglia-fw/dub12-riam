from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from ..models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    username: str
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None
