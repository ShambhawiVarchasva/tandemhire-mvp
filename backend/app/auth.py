# backend/app/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
from .db import get_session
from .models import User
from .schemas import UserCreate, LoginData
from .auth_utils import create_access_token  # if you have JWT logic

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # ✅ Enforce bcrypt password length limit
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long. Please use 72 characters or fewer."
        )

    # Check for existing user
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and save user
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_pw)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "User created successfully", "email": db_user.email}


@router.post("/login")
def login_user(data: LoginData, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # (Optional) JWT token logic
    token = create_access_token({"sub": user.email}) if "create_access_token" in globals() else "fake-token"
    return {"message": "Login successful", "token": token, "email": user.email}

