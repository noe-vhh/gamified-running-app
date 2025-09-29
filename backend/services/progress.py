from ..models.user_challenge import UserChallenge
from datetime import datetime, timedelta

# Tier-based XP multipliers per km
TIER_XP_MULTIPLIERS = {
    "Sprint": 10,
    "Marathon": 15,
    "Ultra": 20,
    "Trailblazer": 25
}

# Streak bonus XP
STREAK_BONUS = 5  # added per consecutive day

# Challenge distance goals (km)
CHALLENGE_GOALS = {
    "Sprint": 50,
    "Marathon": 100,
    "Ultra": 150,
    "Trailblazer": 200
}


def update_challenge_progress(
    user_challenge: UserChallenge, 
    distance_km: float, 
    tier: str, 
    activity_date: datetime = None
) -> float:
    """
    Update a UserChallenge with new activity and calculate XP earned.
    Streak is now based on consecutive days.

    Args:
        user_challenge: UserChallenge object
        distance_km: Distance of the activity in km
        tier: Challenge tier
        activity_date: datetime of activity

    Returns:
        XP earned (float)
    """

    if activity_date is None:
        activity_date = datetime.utcnow()

    # Base XP for distance
    multiplier = TIER_XP_MULTIPLIERS.get(tier, 10)
    xp = distance_km * multiplier

    # Streak logic
    if user_challenge.updated_at:
        last_date = user_challenge.updated_at.date()
        today = activity_date.date()
        if today == last_date + timedelta(days=1):
            # consecutive day → increment streak
            user_challenge.streak += 1
            xp += STREAK_BONUS
        elif today == last_date:
            # same day → do not increment streak, no bonus
            pass
        else:
            # missed day → reset streak
            user_challenge.streak = 1
    else:
        # first activity → start streak
        user_challenge.streak = 1

    # Update progress
    user_challenge.distance_completed_km += distance_km
    user_challenge.xp_earned += xp
    user_challenge.updated_at = activity_date

    # Check completion
    target_distance = CHALLENGE_GOALS.get(tier, 50)
    if user_challenge.distance_completed_km >= target_distance:
        user_challenge.completed = True

    return xp
