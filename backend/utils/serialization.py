from typing import Dict, Any, Optional
from ..models.user import User
from ..models.badge import Badge
from ..models.title import Title

def serialize_user_basic(user: User) -> Dict[str, Any]:
    """
    Serialize basic user information for API responses.
    """
    return {
        "id": user.id,
        "strava_athlete_id": user.strava_athlete_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile": user.profile,
        "profile_medium": user.profile_medium,
        "xp": user.xp,
        "level": user.level,
        "momentum": user.momentum,
        "total_distance_km": user.total_distance_km,
    }

def serialize_badge(badge: Badge) -> Dict[str, Any]:
    """
    Serialize badge information for API responses.
    """
    return {
        "id": badge.id,
        "name": badge.name,
        "description": badge.description,
        "category": badge.category,
        "rarity": badge.rarity,
        "icon_url": badge.icon_url
    }

def serialize_title(title: Title, is_active: bool = False) -> Dict[str, Any]:
    """
    Serialize title information for API responses.
    """
    return {
        "id": title.id,
        "name": title.name,
        "description": title.description,
        "rarity": title.rarity,
        "is_active": is_active
    }
