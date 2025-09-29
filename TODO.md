# 📌 Master TODO

---

## ✅ Completed

### **Project Setup & Infrastructure**

- [x] Setup GitHub repo
- [x] Setup FastAPI backend (base project)
- [x] Setup SQLite DB + migrations (using SQLModel)
- [x] FastAPI backend with auto API docs (available at /docs)

### **Authentication & Security**

- [x] Connect Strava OAuth flow (user auth works)
- [x] User authentication and profile management
- [x] JWT authentication system
- [x] Strava token refresh handling
- [x] Hardcoded fallback secrets ("dev-secret-change-me")

### **Core Backend Functionality**

- [x] Implement activity sync (respects `last_sync_at`)
- [x] New users only sync _future_ activities after registration
- [x] Activity sync endpoint with challenge progress updates
- [x] User profile endpoint with gamification data
- [x] Basic seed script for test users/challenges/badges

### **Gamification System**

- [x] XP awarded per synced activity
- [x] Challenge tiers defined (Sprint, Marathon, Ultra, Trailblazer)
- [x] Momentum concept introduced (XP + streak bonuses)
- [x] Badge/title system implemented (dynamic, stored in DB)
- [x] User model with XP, momentum, badges, titles (JSON fields)
- [x] Challenge system with UserChallenge tracking
- [x] Streak tracking based on consecutive days
- [x] Challenge join/list endpoints
- [x] Rename gamification system
- [x] Migrate badges & titles etc. to DB storage (currently hardcoded)
- [x] Fix Distance Logic: Distance badges should track actual running distance, not XP
- [x] Add Level System: Implement XP-based user levels with level-up rewards
- [x] Award general XP when not in a challenge

---

## 🚨 **PRIORITY 1: CRITICAL FIXES**

### **Security - Critical**

- [ ] Add comprehensive environment variable validation for all secrets
- [ ] Implement input validation using Pydantic models on all API endpoints
- [ ] Add request size limits to prevent DoS attacks
- [ ] Configure CORS properly for frontend integration
- [ ] Remove verbose error messages that could leak sensitive information
- [ ] Add comprehensive error logging and monitoring

### **Performance - Critical**

- [ ] **Fix N+1 Query Problem in `/users/me`** - Separate query for active title instead of using loaded relations
- [ ] **Add Database Connection Pooling** - Current setup creates new connections per request
- [ ] **Add Request Timeout Configuration** - Prevent hanging requests on slow Strava API calls

### **Core Functionality - Critical**

- [ ] Add health check endpoints for monitoring
- [ ] Implement graceful shutdown handling
- [ ] Add request/response logging middleware
- [ ] Add centralized error handling middleware and custom exception classes
- [ ] Implement structured logging with request/response tracking

---

## 🔥 **PRIORITY 2: HIGH IMPACT**

### **Security - High Priority**

- [ ] Implement JWT token refresh mechanism for users
- [ ] Add rate limiting middleware to prevent API abuse
- [ ] Add security headers (HSTS, CSP, X-Frame-Options, etc.)
- [ ] Encrypt sensitive database fields (Strava tokens, etc.)

### **Performance - High Priority**

- [ ] **Add Missing Database Indexes** - Add indexes for frequently queried fields:
  - `user_challenges.user_id` (for challenge lookups)
  - `user_challenges.challenge_id` (for challenge joins)
  - `user_badges.user_id` (for badge lookups)
  - `user_titles.user_id` (for title lookups)
  - `user_titles.is_active` (for active title queries)
  - `challenges.active` (for active challenge filtering)
  - `challenges.tier` (for tier-based filtering)
- [ ] **Implement Caching Layer** - Cache frequently accessed data:
  - User profile data (with TTL)
  - Challenge lists (with invalidation)
  - Badge/title definitions (static data)
- [ ] **Optimize Activity Sync** - Process activities in batches instead of individual loops
- [ ] **Optimize Award System** - Batch database operations in `award_badges_and_titles`
- [ ] **Add Pagination** - Implement pagination for challenge lists and user data

### **API Development - Essential Features**

- [ ] Add comprehensive Pydantic request/response models for all endpoints
- [ ] Badge/title management endpoints (set active title, view badges)
- [ ] User profile update endpoints
- [ ] Challenge progress tracking endpoints
- [ ] Retry logic for Strava API calls
- [ ] User statistics and analytics endpoints
- [ ] Challenge completion and progress tracking endpoints
- [ ] User activity history endpoints

---

## ⚡ **PRIORITY 3: MEDIUM IMPACT**

### **Security - Medium Priority**

- [ ] Implement audit trails for important user actions
- [ ] Add session management and token revocation
- [ ] Set up security monitoring and alerting
- [ ] Add API versioning and deprecation handling
- [ ] Implement proper secret rotation strategy

### **Performance - Medium Priority**

- [ ] **Implement Async/Await** - Convert blocking operations to async for better concurrency
- [ ] **Add Database Query Optimization** - Use `selectinload` consistently for related data
- [ ] **Implement Background Tasks** - Move heavy operations to background workers
- [ ] **Add Response Compression** - Enable gzip compression for API responses
- [ ] **Optimize Serialization** - Cache serialized objects and reduce redundant processing
- [ ] **Add Database Query Logging** - Monitor slow queries and optimize them
- [ ] **Optimize Strava API Calls** - Add request batching and connection reuse

### **Backend Infrastructure**

- [ ] Set up database migration system using Alembic
- [ ] Add API versioning strategy
- [ ] Implement background task processing for heavy operations
- [ ] Add circuit breaker pattern for external API calls

---

## 📱 **PRIORITY 4: FRONTEND & USER EXPERIENCE**

### **Mobile Frontend**

- [ ] Expo + React Native base app (iOS + Android)
- [ ] NativeWind (Tailwind styling)
- [ ] Zustand for state management
- [ ] React Query for API sync
- [ ] Push notifications (streak reminders, friend activities, milestones)

### **Core Gameplay Enhancements**

- [ ] Review and optimize momentum system
- [ ] Implement soft delete functionality

### **Developer Tools & Maintenance**

- [ ] Enhanced debugging and testing scripts
- [ ] Database inspection and maintenance tools
- [ ] Performance monitoring dashboard
- [ ] Automated testing setup and CI/CD pipeline
- [ ] Docker containerization for consistent deployments
- [ ] Environment-specific configuration management
- [ ] Database backup/restore scripts
- [ ] Code documentation standards and maintenance utilities

---

## 🚀 **PRIORITY 5: SCALING & OPTIMIZATION**

### **Performance - Low Priority**

- [ ] **Add Database Query Caching** - Cache expensive queries with Redis
- [ ] **Optimize JSON Parsing** - Use faster JSON libraries for large responses
- [ ] **Add Response Caching Headers** - Cache static responses appropriately
- [ ] **Implement Database Read Replicas** - Separate read/write operations
- [ ] **Add Performance Monitoring** - Track response times and database performance
- [ ] **Implement Lazy Loading** - Load related data only when needed

### **Backend Scaling**

- [ ] Migrate to PostgreSQL for production scaling
- [ ] Backup/restore strategy
- [ ] Job queue for Strava sync (Celery / RQ)
- [ ] Analytics + monitoring (retention, churn, engagement)
- [ ] CDN for images/media
- [ ] API documentation security review

---

## 👥 **PRIORITY 6: SOCIAL FEATURES**

### **Social System**

- [ ] Friends system
- [ ] Friends discovery, search & requests
- [ ] Clubs system
- [ ] Club discovery & search
- [ ] Community System (Possibly teams etc. for non club members not wanting Solo experience)

### **Leaderboards**

- [ ] Solo level leaderboard (XP-based)
- [ ] Internal Club leaderboards (internal ranking of members by XP)
- [ ] Club vs. Club system (fair rules: both clubs complete same challenge)
- [ ] Club Regional leaderboards (local, city, national, global)

---

## 🎮 **PRIORITY 7: GAMIFICATION ENHANCEMENTS**

### **Loop Enhancements**

- [ ] Profile viewing (Player, friends, club)
- [ ] Profile customization (themes, badges, frames)
- [ ] Prestige / Seasons system (reset + climb ranks)
- [ ] Auto-generate solo challenges (tiered: Sprint, Marathon, Ultra, Trailblazer)

### **Rewards System**

- [ ] Seasonal rewards (limited badges/titles per season)
- [ ] Achievement chains (progressive milestones)
- [ ] Club trophies & banners for achievements
- [ ] Seasonal resets for club leaderboards
- [ ] Weighted scoring system so less-fit users can still contribute meaningfully
