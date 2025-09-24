from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
import requests

router = APIRouter()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

print("STRAVA_CLIENT_ID:", STRAVA_CLIENT_ID)
print("STRAVA_CLIENT_SECRET:", STRAVA_CLIENT_SECRET)
print("STRAVA_REDIRECT_URI:", STRAVA_REDIRECT_URI)

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
    response = requests.post(token_url, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })
    token_data = response.json()
    return token_data