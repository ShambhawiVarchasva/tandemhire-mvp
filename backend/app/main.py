# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, engine
from .models import User, Candidate, Job
from .jack_flow import router as jack_router
from .auth import router as auth_router  # ✅ Include auth routes

app = FastAPI(title="TandemHire API")

# CORS setup
origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
init_db()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])  # ✅ Added auth endpoints
app.include_router(jack_router, prefix="/jack", tags=["jack"])

