# backend/main.py
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

# ───── Load environment variables BEFORE importing routes ─────
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

print("STRAVA_CLIENT_ID:", os.getenv("STRAVA_CLIENT_ID"))
print("STRAVA_REDIRECT_URI:", os.getenv("STRAVA_REDIRECT_URI"))

# ───── Now import routes and database ─────
from .routes import auth, users, challenges, activity_sync
from .db import create_db_and_tables

# ───── Lifespan for startup/shutdown ─────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # Shutdown logic (optional)

# ───── Create FastAPI app ─────
app = FastAPI(title="Gamified Running App MVP", lifespan=lifespan)

# ───── Include routers ─────
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(challenges.router, prefix="/challenges")
app.include_router(activity_sync.router, prefix="/activities")

# ───── Root endpoint ─────
@app.get("/")
def root():
    return {"message": "Welcome to Gamified Running App MVP"}