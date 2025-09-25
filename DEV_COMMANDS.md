Development Reference

---

## 1. Start Backend

    venv\Scripts\activate

# Run server

    uvicorn backend.main:app --reload

    uvicorn backend.main:app --reload --reload-dir backend  # Watch only backend folder

---

## 2. Backend URLs (Localhost)

    Home / Health Check http://127.0.0.1:8000/ Simple root message
    Strava OAuth Login http://127.0.0.1:8000/auth/strava/login Redirects to Strava login
    Swagger UI / Docs http://127.0.0.1:8000/docs Test all endpoints interactively
    JWT-Protected User Profile http://127.0.0.1:8000/users/me Requires JWT from Strava login callback

---

## 3. Database Inspection (SQLite)

    python -m backend.scripts.list_users
