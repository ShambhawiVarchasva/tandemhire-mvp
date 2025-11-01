# backend/app/jack_flow.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select
from .models import Candidate
import os
import uuid

router = APIRouter()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/tandemhire_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_resume/{user_id}")
async def upload_resume(user_id: int, file: UploadFile = File(...)):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    contents = await file.read()
    with open(path, "wb") as f:
        f.write(contents)
    from .db import engine
    with Session(engine) as session:
        statement = select(Candidate).where(Candidate.user_id == user_id)
        res = session.exec(statement).first()
        if not res:
            c = Candidate(user_id=user_id, resume_path=path)
            session.add(c)
        else:
            res.resume_path = path
        session.commit()
    return {"ok": True, "path": path}

@router.post("/onboard/{user_id}")
async def onboard(user_id: int, answers: dict):
    from .db import engine
    with Session(engine) as session:
        statement = select(Candidate).where(Candidate.user_id == user_id)
        cand = session.exec(statement).first()
        if not cand:
            cand = Candidate(user_id=user_id)
            session.add(cand)
        cand.headline = answers.get("current_title")
        cand.location = answers.get("location")
        cand.salary_expectation = answers.get("salary_expectation")
        cand.skills = answers.get("skills")
        session.commit()
    summary = (
        f"{answers.get('current_title','')} with {answers.get('years_experience','?')} years. "
        f"Skills: {answers.get('skills','')}. Location: {answers.get('location','')}. "
        f"Salary: {answers.get('salary_expectation','')}"
    )
    return {"ok": True, "summary": summary}
