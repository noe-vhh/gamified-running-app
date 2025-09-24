# Development Reference

```bash
uvicorn backend.main:app --reload
```

---

2. Backend URLs (Localhost)

Home / Health Check:
http://127.0.0.1:8000/

Strava OAuth Login:
http://127.0.0.1:8000/auth/strava/login

JWT-Protected User Profile:
Requires the access token returned from Strava login:
http://127.0.0.1:8000/users/me

---

3. Database Inspection (SQLite)

List all users stored in the database:

```bash
python -m backend.scripts.list_users
```
