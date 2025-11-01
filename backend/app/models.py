# backend/app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    name: Optional[str] = None
    hashed_password: Optional[str] = None
    role: str = "candidate"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    headline: Optional[str] = None
    location: Optional[str] = None
    salary_expectation: Optional[str] = None
    skills: Optional[str] = None
    resume_path: Optional[str] = None

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: Optional[str] = None
    title: str
    location: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
