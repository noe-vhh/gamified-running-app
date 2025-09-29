from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session, select
import os

from ..db import engine, get_session
from ..models.user import User
from ..models.badge import Badge
from ..models.title import Title
from ..models.user_badge import UserBadge
from ..models.user_title import UserTitle
from ..utils.dependencies import get_current_user

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

@router.get("/me")
def read_users_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Return safe user fields for dashboard / frontend.
    """
    # Get user's badges
    user_badges = session.exec(
        select(Badge).join(UserBadge).where(UserBadge.user_id == current_user.id)
    ).all()
    
    # Get user's titles
    user_titles = session.exec(
        select(Title).join(UserTitle).where(UserTitle.user_id == current_user.id)
    ).all()
    
    # Get active title
    active_title = session.exec(
        select(Title).join(UserTitle).where(
            UserTitle.user_id == current_user.id,
            UserTitle.is_active == True
        )
    ).first()
    
    return {
        "id": current_user.id,
        "strava_athlete_id": current_user.strava_athlete_id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "profile": current_user.profile,
        "profile_medium": current_user.profile_medium,
        "xp": current_user.xp,
        "level": current_user.level,
        "momentum": current_user.momentum,
        "total_distance_km": current_user.total_distance_km,
        "badges": [
            {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "category": badge.category,
                "rarity": badge.rarity,
                "icon_url": badge.icon_url
            }
            for badge in user_badges
        ],
        "titles": [
            {
                "id": title.id,
                "name": title.name,
                "description": title.description,
                "rarity": title.rarity,
                "is_active": any(ut.title_id == title.id and ut.is_active for ut in current_user.user_titles)
            }
            for title in user_titles
        ],
        "active_title": {
            "id": active_title.id,
            "name": active_title.name,
            "description": active_title.description,
            "rarity": active_title.rarity
        } if active_title else None
    }