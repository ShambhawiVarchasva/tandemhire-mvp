# backend/app/main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from .db import init_db, engine
from .models import User, Candidate, Job
from .schemas import UserCreate, Token, LoginData, JobCreate
from .auth import hash_password, verify_password, create_access_token
from .jack_flow import router as jack_router

app = FastAPI(title="TandemHire API")

origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jack_router, prefix="/jack", tags=["jack"])

@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
        jobs = session.exec(select(Job)).all()
        if not jobs:
            session.add(Job(title="Backend Engineer", company="Acme", location="Remote", description="Build APIs", required_skills="python,fastapi,sql"))
            session.add(Job(title="Frontend Engineer", company="DesignCo", location="Bengaluru", description="React apps", required_skills="react,nextjs,css"))
            session.commit()

@app.post("/auth/register", response_model=Token)
def register(data: UserCreate):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == data.email)).first()
        if existing:
            raise HTTPException(status_code=400, detail="User exists")
        hashed = hash_password(data.password)
        u = User(email=data.email, name=data.name, hashed_password=hashed, role="candidate")
        session.add(u)
        session.commit()
        session.refresh(u)
        token = create_access_token({"user_id": u.id, "email": u.email})
        return {"access_token": token, "user_id": u.id}

@app.post("/auth/login", response_model=Token)
def login(data: LoginData):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == data.email)).first()
        if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"user_id": user.id, "email": user.email})
        return {"access_token": token, "user_id": user.id}

@app.get("/jobs")
def list_jobs():
    with Session(engine) as session:
        jobs = session.exec(select(Job)).all()
        return jobs

@app.post("/jobs")
def create_job(job: JobCreate):
    with Session(engine) as session:
        j = Job(title=job.title, company=job.company, location=job.location, description=job.description, required_skills=job.required_skills)
        session.add(j)
        session.commit()
        session.refresh(j)
        return j

@app.get("/match/{user_id}")
def match_jobs(user_id: int):
    with Session(engine) as session:
        cand = session.exec(select(Candidate).where(Candidate.user_id == user_id)).first()
        if not cand:
            raise HTTPException(status_code=404, detail="Candidate not found")
        cand_skills = {s.strip().lower() for s in (cand.skills or "").split(",") if s.strip()}
        jobs = session.exec(select(Job)).all()
        scored = []
        for j in jobs:
            req_skills = {s.strip().lower() for s in (j.required_skills or "").split(",") if s.strip()}
            overlap = len(cand_skills & req_skills)
            scored.append({"job": {
                        "id": j.id,
                        "title": j.title,
                        "company": j.company,
                        "location": j.location,
                        "description": j.description,
                        "required_skills": j.required_skills
                    }, "score": overlap})
        scored_sorted = sorted(scored, key=lambda r: r["score"], reverse=True)
        return scored_sorted[:20]
