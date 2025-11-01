from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
from .db import get_session
from .models import User
from .schemas import UserCreate, LoginData
from .auth_utils import create_access_token

router = APIRouter()

# ✅ Use bcrypt safely
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    raw_password = user.password.strip()
    if not raw_password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")

    # ✅ Ensure UTF-8 encoding
    encoded_pw = raw_password.encode("utf-8")
    print(f"Password length (bytes): {len(encoded_pw)}")

    # ✅ Truncate if too long (bcrypt ignores beyond 72 anyway)
    if len(encoded_pw) > 72:
        encoded_pw = encoded_pw[:72]
        raw_password = encoded_pw.decode("utf-8", errors="ignore")

    # ✅ Check if email already registered
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Hash safely
    hashed_password = pwd_context.hash(raw_password)
    db_user = User(email=user.email, name=user.name, password_hash=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return {"message": "User created successfully", "email": db_user.email}


@router.post("/login")
def login_user(data: LoginData, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not pwd_context.verify(data.password.strip(), user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"message": "Login successful", "token": token, "email": user.email}

