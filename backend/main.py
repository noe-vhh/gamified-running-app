from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os

# Force load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Debugging: print loaded environment variables
env_values = dotenv_values(env_path)
print("Loaded .env values:", env_values)

from fastapi import FastAPI
from .routes import auth

app = FastAPI(title="Gamified Running App MVP")

app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Welcome to Gamified Running App MVP"}