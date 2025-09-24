from dotenv import load_dotenv
from pathlib import Path
import os

# Force load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from .routes import auth

app = FastAPI(title="Gamified Running App MVP")

app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Welcome to Gamified Running App MVP"}