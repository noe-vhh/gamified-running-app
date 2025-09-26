from typing import List
import os
import requests
from datetime import datetime
from ..models.user import User
from ..db import engine
from sqlmodel import Session

STRAVA_API_URL = "https://www.strava.com/api/v3"
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")


def refresh_access_token(user: User, session: Session) -> str:
    """
    Refresh Strava access token using the refresh_token.
    Updates the user record in the DB.
    """
    data = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": user.refresh_token
    }
    resp = requests.post(f"{STRAVA_API_URL}/oauth/token", data=data)
    if resp.status_code != 200:
        raise Exception(f"Failed to refresh Strava token: {resp.json()}")

    token_data = resp.json()
    user.access_token = token_data["access_token"]
    user.refresh_token = token_data.get("refresh_token", user.refresh_token)
    expires_at = token_data.get("expires_at")
    user.token_expires_at = datetime.utcfromtimestamp(expires_at) if expires_at else None

    # Save updated tokens
    session.add(user)
    session.commit()
    session.refresh(user)

    return user.access_token


def fetch_user_activities(user: User, after_timestamp: int = None) -> List[dict]:
    """
    Fetch Strava activities for a user.
    Auto-refreshes access token if expired or unauthorized.
    """
    with Session(engine) as session:
        # Refresh token if expired
        if user.token_expires_at and datetime.utcnow() >= user.token_expires_at:
            user.access_token = refresh_access_token(user, session)

        headers = {"Authorization": f"Bearer {user.access_token}"}
        params = {}
        if after_timestamp:
            params["after"] = after_timestamp

        response = requests.get(f"{STRAVA_API_URL}/athlete/activities", headers=headers, params=params)

        # If unauthorized, try refreshing token once
        if response.status_code == 401:
            user.access_token = refresh_access_token(user, session)
            headers = {"Authorization": f"Bearer {user.access_token}"}
            response = requests.get(f"{STRAVA_API_URL}/athlete/activities", headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Strava API error: {response.json()}")

        return response.json()