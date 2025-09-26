from ..models.user_challenge import UserChallenge
from ..models.user import User

TIER_MULTIPLIERS = {
    "Sprint": 10,
    "Marathon": 15,
    "Ultra": 20,
    "Trailblazer": 25
}
STREAK_BONUS = 5

def update_challenge_progress(user_challenge, distance_km, tier):
    """
    Update a UserChallenge with a new activity.
    Returns XP gained from this activity.
    """
    # Example XP calculation by tier
    tier_xp_multiplier = {"Sprint": 15, "Marathon": 20, "Ultra": 25}
    xp = distance_km * tier_xp_multiplier.get(tier, 10)

    # Update challenge progress
    user_challenge.distance_completed_km += distance_km
    user_challenge.streak += 1

    # Determine completion threshold per tier
    challenge_goals = {"Sprint": 50, "Marathon": 70, "Ultra": 100}  # km
    if user_challenge.distance_completed_km >= challenge_goals.get(tier, 50):
        user_challenge.completed = True

    return xp