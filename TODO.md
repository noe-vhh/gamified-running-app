# 📌 Master TODO

---

## ✅ Completed

- [x] Setup GitHub repo
- [x] Setup FastAPI backend (base project)
- [x] Setup SQLite DB + migrations (using SQLModel)
- [x] Connect Strava OAuth flow (user auth works)
- [x] User authentication and profile management
- [x] Implement activity sync (respects `last_sync_at`)
- [x] New users only sync _future_ activities after registration
- [x] XP awarded per synced activity
- [x] Challenge tiers defined (Sprint, Marathon, Ultra, Trailblazer)
- [x] Momentum concept introduced (XP + streak bonuses)
- [x] Badge/title system implemented (dynamic, stored in DB)
- [x] User model with XP, momentum, badges, titles (JSON fields)
- [x] Challenge system with UserChallenge tracking
- [x] Streak tracking based on consecutive days
- [x] Activity sync endpoint with challenge progress updates
- [x] Challenge join/list endpoints
- [x] User profile endpoint with gamification data
- [x] Basic seed script for test users/challenges/badges
- [x] JWT authentication system
- [x] Strava token refresh handling
- [x] FastAPI backend with auto API docs (available at /docs)
- [x] Rename gamification system\
- [x] Migrate badges & titles etc. to DB storage (currently hardcoded)

---

## **Core Gameplay**

- [ ] Fix Distance Logic: Distance badges should track actual running distance, not XP\
- [ ] Award Management: Allow users to set active titles
- [ ] Award Display: Create endpoints to view user's badges and titles

- [ ] Add Level System: Implement XP-based user levels with level-up rewards
- [ ] Award general XP when not in a challenge

- [ ] Check momentum system
- [ ] Reason for momentum system

---

## **Tech / Backend**

- [ ] Migrate to PostgreSQL for production scaling
- [ ] Add comprehensive error handling & logging
- [ ] Add rate limiting for API endpoints
- [ ] Job queue for Strava sync (Celery / RQ)
- [ ] Analytics + monitoring (retention, churn, engagement)
- [ ] CDN for images/media

---

## **Mobile Frontend**

- [ ] Expo + React Native base app (iOS + Android)
- [ ] NativeWind (Tailwind styling)
- [ ] Zustand for state management
- [ ] React Query for API sync
- [ ] Push notifications (streak reminders, friend activities, milestones)

---

## **Social**

- [ ] Friends system
- [ ] Friends discovery, search & requests
- [ ] Clubs system
- [ ] Club discovery & search
- [ ] Community System (Possibly teams etc. for non club members not wanting Solo experience)

---

## **Leaderboards**

- [ ] Solo level leaderboard (XP-based)
- [ ] Internal Club leaderboards (internal ranking of members by XP)
- [ ] Club vs. Club system (fair rules: both clubs complete same challenge)
- [ ] CLub Regional leaderboards (local, city, national, global)

---

## **Loop Enhancements**

- [ ] Profile viewing (Player, friends, club)
- [ ] Profile customization (themes, badges, frames)
- [ ] Prestige / Seasons system (reset + climb ranks)
- [ ] Auto-generate solo challenges (tiered: Sprint, Marathon, Ultra, Trailblazer)

---

## **Rewards**

- [ ] Seasonal rewards (limited badges/titles per season)
- [ ] Achievement chains (progressive milestones)
- [ ] Club trophies & banners for achievements
- [ ] Seasonal resets for club leaderboards
- [ ] Weighted scoring system so less-fit users can still contribute meaningfully
