from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session
import os

from ..db import engine
from ..models.user import User
from ..utils.dependencies import get_current_user

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Return safe user fields for dashboard / frontend.
    """
    return {
        "id": current_user.id,
        "strava_athlete_id": current_user.strava_athlete_id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "profile": current_user.profile,
        "profile_medium": current_user.profile_medium,
        "xp": current_user.xp,
        "momentum": current_user.momentum,
        "badges": current_user.badges,
        "titles": current_user.titles
    }