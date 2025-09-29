from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
import os

from ..db import engine, get_session
from ..models.user import User
from ..models.badge import Badge
from ..models.title import Title
from ..models.user_badge import UserBadge
from ..models.user_title import UserTitle
from ..utils.dependencies import get_current_user
from ..utils.security import SECRET_KEY, ALGORITHM
from ..utils.serialization import serialize_user_basic, serialize_badge, serialize_title

router = APIRouter()
security = HTTPBearer()

@router.get("/me")
def read_users_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Return safe user fields for dashboard / frontend.
    """
    # Optimized query: Get user with all related data in one go
    user_with_relations = session.exec(
        select(User)
        .options(
            selectinload(User.user_badges).selectinload(UserBadge.badge),
            selectinload(User.user_titles).selectinload(UserTitle.title)
        )
        .where(User.id == current_user.id)
    ).first()
    
    if not user_with_relations:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get active title
    active_title = session.exec(
        select(Title).join(UserTitle).where(
            UserTitle.user_id == current_user.id,
            UserTitle.is_active == True
        )
    ).first()
    
    # Serialize user data
    user_data = serialize_user_basic(user_with_relations)
    
    # Serialize badges
    badges = [serialize_badge(ub.badge) for ub in user_with_relations.user_badges]
    
    # Serialize titles with active status
    titles = []
    for ut in user_with_relations.user_titles:
        title_data = serialize_title(ut.title, ut.is_active)
        titles.append(title_data)
    
    # Add badges, titles, and active title to response
    user_data.update({
        "badges": badges,
        "titles": titles,
        "active_title": serialize_title(active_title) if active_title else None
    })
    
    return user_data