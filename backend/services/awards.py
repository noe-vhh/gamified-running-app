from typing import List
from ..models.user import User
from ..models.user_challenge import UserChallenge

# Define thresholds for badges
DISTANCE_MILESTONES = [10, 25, 50, 100]  # km
STREAK_MILESTONES = [3, 7, 14]  # days

def award_badges_and_titles(user: User, user_challenges: List[UserChallenge]):
    new_badges = []
    new_titles = []

    # --- Distance Milestones ---
    for milestone in DISTANCE_MILESTONES:
        if user.xp >= milestone * 10:  # example: 1 km = 10 XP
            badge_name = f"{milestone}km Milestone"
            if badge_name not in (user.badges or []):
                user.badges.append(badge_name)
                new_badges.append(badge_name)

    # --- Challenge Completion Badges ---
    for uc in user_challenges:
        if uc.completed and uc.challenge:  # make sure challenge relationship is loaded
            badge_name = f"{uc.challenge.tier} Challenge Complete"
            if badge_name not in (user.badges or []):
                user.badges.append(badge_name)
                new_badges.append(badge_name)

    # --- Titles ---
    if "Steady Strider" not in (user.titles or []) and any(uc.completed for uc in user_challenges):
        user.titles.append("Steady Strider")
        new_titles.append("Steady Strider")

    tiers_completed = {uc.challenge.tier for uc in user_challenges if uc.completed and uc.challenge}
    if "Tier Master" not in (user.titles or []) and len(tiers_completed) == 4:  # all tiers completed
        user.titles.append("Tier Master")
        new_titles.append("Tier Master")

    return new_badges, new_titles