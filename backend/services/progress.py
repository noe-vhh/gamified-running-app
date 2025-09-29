from ..models.user_challenge import UserChallenge
from ..models.user import User
from datetime import datetime, timedelta
import math

# Base XP system - everyone gets XP for running
BASE_XP_PER_KM = 10  # Base XP for all running activities
CHALLENGE_XP_BONUS = 4  # Additional XP per km when in challenges

# Fair tier-based XP multipliers (small bonuses for harder challenges)
TIER_XP_MULTIPLIERS = {
    "Sprint": 1.0,      # 10 XP/km (base)
    "Marathon": 1.2,    # 12 XP/km (+20% bonus)
    "Ultra": 1.4,       # 14 XP/km (+40% bonus)
    "Trailblazer": 1.6  # 16 XP/km (+60% bonus)
}

# Streak bonus XP
STREAK_BONUS = 10  # added per consecutive day

# Challenge distance goals (km)
CHALLENGE_GOALS = {
    "Sprint": 50,
    "Marathon": 100,
    "Ultra": 150,
    "Trailblazer": 200
}

# Level cap
MAX_LEVEL = 100


def calculate_level(xp: int) -> int:
    """
    Calculate user level based on XP.
    Level progression: Level = sqrt(XP / 20) + 1 (BALANCED: 5x easier than original)
    This creates a balanced progression curve.
    Level is capped at MAX_LEVEL (100).
    """
    calculated_level = int(math.sqrt(xp / 20)) + 1
    return min(calculated_level, MAX_LEVEL)


def xp_for_next_level(current_level: int) -> int:
    """
    Calculate XP required for the next level.
    Returns None if user is at max level.
    """
    if current_level >= MAX_LEVEL:
        return None
    return ((current_level + 1) * 20) ** 2


def check_level_up(user: User) -> bool:
    """
    Check if user has leveled up and update their level.
    Returns True if user leveled up, False otherwise.
    Users at max level cannot level up further.
    """
    new_level = calculate_level(user.xp)
    if new_level > user.level and user.level < MAX_LEVEL:
        user.level = new_level
        return True
    return False


def is_at_max_level(user: User) -> bool:
    """
    Check if user has reached the maximum level.
    """
    return user.level >= MAX_LEVEL


def calculate_base_xp(distance_km: float, in_challenge: bool = False) -> float:
    """
    Calculate base XP for a running activity.
    
    Args:
        distance_km: Distance of the activity in km
        in_challenge: Whether the user is participating in a challenge
        
    Returns:
        Base XP earned
    """
    base_xp = distance_km * BASE_XP_PER_KM
    if in_challenge:
        base_xp += distance_km * CHALLENGE_XP_BONUS
    return base_xp


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

    # Calculate XP with fair tier multipliers
    base_xp = calculate_base_xp(distance_km, in_challenge=True)
    tier_multiplier = TIER_XP_MULTIPLIERS.get(tier, 1.0)
    xp = base_xp * tier_multiplier

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
