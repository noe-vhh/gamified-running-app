from typing import List
import requests
from ..models.user import User

STRAVA_API_URL = "https://www.strava.com/api/v3"

def fetch_user_activities(user: User, after_timestamp: int = None) -> List[dict]:
    """
    Fetch Strava activities for a user.
    :param user: User object with access_token
    :param after_timestamp: optional UNIX timestamp to fetch activities since
    :return: list of activities
    """
    headers = {"Authorization": f"Bearer {user.access_token}"}
    params = {}
    if after_timestamp:
        params["after"] = after_timestamp

    response = requests.get(f"{STRAVA_API_URL}/athlete/activities", headers=headers, params=params)
    if response.status_code != 200:
        # could add auto-refresh token logic here
        raise Exception(f"Strava API error: {response.json()}")
    
    return response.json()