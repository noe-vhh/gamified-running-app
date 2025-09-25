# backend/routes/auth.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import os
import requests
from datetime import datetime
from sqlmodel import select, Session

from ..db import engine
from ..models.user import User
from ..utils.security import create_access_token

router = APIRouter()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

@router.get("/strava/login")
def strava_login():
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&scope=read,activity:read_all"
    )
    return RedirectResponse(url)

@router.get("/strava/callback")
def strava_callback(code: str):
    token_url = "https://www.strava.com/oauth/token"
    resp = requests.post(token_url, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })
    token_data = resp.json()

    if resp.status_code != 200:
        # bubble up error for debugging
        raise HTTPException(status_code=400, detail=token_data)

    athlete = token_data.get("athlete")
    if not athlete:
        raise HTTPException(status_code=400, detail="No athlete in Strava response")

    expires_at = token_data.get("expires_at")
    token_expires_dt = datetime.utcfromtimestamp(expires_at) if expires_at else None

    # Upsert user
    with Session(engine) as session:
        statement = select(User).where(User.strava_athlete_id == athlete["id"])
        existing = session.exec(statement).first()

        if existing:
            user = existing
            # update fields & tokens
            user.username = athlete.get("username") or user.username
            user.first_name = athlete.get("firstname") or user.first_name
            user.last_name = athlete.get("lastname") or user.last_name
            user.city = athlete.get("city") or user.city
            user.state = athlete.get("state") or user.state
            user.country = athlete.get("country") or user.country
            user.bio = athlete.get("bio") or user.bio
            user.premium = athlete.get("premium") or user.premium
            user.sex = athlete.get("sex") or user.sex
            user.weight = athlete.get("weight") or user.weight
            user.profile = athlete.get("profile") or user.profile
            user.profile_medium = athlete.get("profile_medium") or user.profile_medium
            user.access_token = token_data.get("access_token")
            user.refresh_token = token_data.get("refresh_token")
            user.token_expires_at = token_expires_dt
            user.updated_at = datetime.utcnow()
        else:
            user = User(
                strava_athlete_id=athlete["id"],
                username=athlete.get("username"),
                first_name=athlete.get("firstname"),
                last_name=athlete.get("lastname"),
                bio=athlete.get("bio"),
                city=athlete.get("city"),
                state=athlete.get("state"),
                country=athlete.get("country"),
                premium=athlete.get("premium"),
                sex=athlete.get("sex"),
                weight=athlete.get("weight"),
                profile=athlete.get("profile"),
                profile_medium=athlete.get("profile_medium"),
                access_token=token_data.get("access_token"),
                refresh_token=token_data.get("refresh_token"),
                token_expires_at=token_expires_dt
            )
            session.add(user)

        session.commit()
        session.refresh(user)

    # create a simple JWT for your frontend to use
    jwt_token = create_access_token({"user_id": user.id, "strava_athlete_id": user.strava_athlete_id})

    # Return only safe user fields
    user_payload = {
        "id": user.id,
        "strava_athlete_id": user.strava_athlete_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile": user.profile,
        "profile_medium": user.profile_medium,
        "xp": user.xp,
        "momentum": user.momentum
    }

    return {"access_token": jwt_token, "token_type": "bearer", "user": user_payload}