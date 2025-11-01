# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int

class LoginData(BaseModel):
    email: str
    password: str

class JobCreate(BaseModel):
    title: str
    company: Optional[str]
    location: Optional[str]
    description: Optional[str]
    required_skills: Optional[str]
