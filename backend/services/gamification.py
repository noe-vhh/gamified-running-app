from ..models.user_challenge import UserChallenge

# Tier-based XP multipliers per km
TIER_XP_MULTIPLIERS = {
    "Sprint": 10,
    "Marathon": 15,
    "Ultra": 20,
    "Trailblazer": 25
}

# Streak bonus XP
STREAK_BONUS = 5  # optional, added per consecutive activity

# Challenge distance goals (km)
CHALLENGE_GOALS = {
    "Sprint": 50,
    "Marathon": 100,
    "Ultra": 150,
    "Trailblazer": 200
}


def update_challenge_progress(user_challenge: UserChallenge, distance_km: float, tier: str) -> float:
    """
    Update a UserChallenge with new activity distance and calculate XP earned.
    Returns XP gained from this activity.

    Args:
        user_challenge: UserChallenge object
        distance_km: Distance of the activity in km
        tier: Challenge tier (Sprint, Marathon, Ultra, etc.)

    Returns:
        XP earned (float)
    """

    # Calculate base XP for the distance
    multiplier = TIER_XP_MULTIPLIERS.get(tier, 10)
    xp = distance_km * multiplier

    # Optional: streak bonus (1 XP per consecutive day)
    if user_challenge.streak > 0:
        xp += STREAK_BONUS

    # Update challenge progress
    user_challenge.distance_completed_km += distance_km
    user_challenge.streak += 1  # increment streak by 1 per activity
    user_challenge.xp_earned += xp

    # Mark challenge as completed if distance target reached
    target_distance = CHALLENGE_GOALS.get(tier, 50)
    if user_challenge.distance_completed_km >= target_distance:
        user_challenge.completed = True

    return xp