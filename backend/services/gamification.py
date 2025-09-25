from ..models.user_challenge import UserChallenge
from ..models.user import User

TIER_MULTIPLIERS = {
    "Sprint": 10,
    "Marathon": 15,
    "Ultra": 20,
    "Trailblazer": 25
}
STREAK_BONUS = 5

def update_challenge_progress(user_challenge: UserChallenge, distance_completed_km: float, tier: str):
    # update distance
    user_challenge.distance_completed_km += distance_completed_km

    # simple streak: +1
    user_challenge.streak += 1

    # XP earned
    xp = distance_completed_km * TIER_MULTIPLIERS.get(tier, 10) + user_challenge.streak * STREAK_BONUS
    user_challenge.xp_earned += xp

    # optionally mark completed if target reached
    if hasattr(user_challenge, "challenge") and user_challenge.distance_completed_km >= user_challenge.challenge.distance_target_km:
        user_challenge.completed = True

    return xp