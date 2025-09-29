from typing import List, Tuple
import json
from sqlmodel import Session, select
from ..models.user import User
from ..models.user_challenge import UserChallenge
from ..models.badge import Badge, BadgeCategory
from ..models.title import Title
from ..models.user_badge import UserBadge
from ..models.user_title import UserTitle

def award_badges_and_titles(user: User, user_challenges: List[UserChallenge], session: Session) -> Tuple[List[str], List[str]]:
    """
    Award badges and titles to a user based on their progress.
    Returns lists of newly awarded badge and title names.
    """
    new_badges = []
    new_titles = []

    # Get user's current badges and titles
    user_badges = session.exec(
        select(Badge).join(UserBadge).where(UserBadge.user_id == user.id)
    ).all()
    user_titles = session.exec(
        select(Title).join(UserTitle).where(UserTitle.user_id == user.id)
    ).all()
    
    user_badge_names = {badge.name for badge in user_badges}
    user_title_names = {title.name for title in user_titles}

    # --- Distance Milestone Badges ---
    distance_badges = session.exec(
        select(Badge).where(Badge.category == BadgeCategory.DISTANCE)
    ).all()
    
    for badge in distance_badges:
        if badge.name not in user_badge_names:
            requirements = json.loads(badge.requirements)
            if requirements["type"] == "distance" and user.total_distance_km >= requirements["distance_required"]:
                # Award the badge
                user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
                session.add(user_badge)
                new_badges.append(badge.name)

    # --- Streak Badges ---
    streak_badges = session.exec(
        select(Badge).where(Badge.category == BadgeCategory.STREAK)
    ).all()
    
    for badge in streak_badges:
        if badge.name not in user_badge_names:
            requirements = json.loads(badge.requirements)
            if requirements["type"] == "streak":
                # Check if user has the required streak
                max_streak = max((uc.streak for uc in user_challenges), default=0)
                if max_streak >= requirements["threshold"]:
                    user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
                    session.add(user_badge)
                    new_badges.append(badge.name)

    # --- Challenge Completion Badges ---
    challenge_badges = session.exec(
        select(Badge).where(Badge.category == BadgeCategory.CHALLENGE)
    ).all()
    
    for badge in challenge_badges:
        if badge.name not in user_badge_names:
            requirements = json.loads(badge.requirements)
            if requirements["type"] == "challenge_tier":
                # Check if user completed a challenge of this tier
                tier_completed = any(
                    uc.completed and uc.challenge and uc.challenge.tier == requirements["tier"]
                    for uc in user_challenges
                )
                if tier_completed:
                    user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
                    session.add(user_badge)
                    new_badges.append(badge.name)

    # --- Titles ---
    titles = session.exec(select(Title)).all()
    
    for title in titles:
        if title.name not in user_title_names:
            requirements = json.loads(title.requirements)
            
            should_award = False
            
            if requirements["type"] == "challenge_completion":
                # Award if user completed at least the required number of challenges
                completed_count = sum(1 for uc in user_challenges if uc.completed)
                should_award = completed_count >= requirements["count"]
                
            elif requirements["type"] == "all_tiers_completed":
                # Award if user completed challenges in all required tiers
                tiers_completed = {
                    uc.challenge.tier for uc in user_challenges 
                    if uc.completed and uc.challenge
                }
                should_award = all(tier in tiers_completed for tier in requirements["tiers"])
            
            if should_award:
                user_title = UserTitle(
                    user_id=user.id, 
                    title_id=title.id,
                    is_active=False  # User can choose which title to display
                )
                session.add(user_title)
                new_titles.append(title.name)

    return new_badges, new_titles