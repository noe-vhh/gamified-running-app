# backend/main.py
from dotenv import load_dotenv
from pathlib import Path

# Force load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from .routes import auth, users, challenges, activity_sync
from .db import create_db_and_tables

app = FastAPI(title="Gamified Running App MVP")

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(challenges.router, prefix="/challenges")
app.include_router(activity_sync.router, prefix="/activities")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Welcome to Gamified Running App MVP"}