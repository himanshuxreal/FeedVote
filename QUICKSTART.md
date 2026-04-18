# FeedVote - Quick Start Guide

**Last Updated:** 18th April 2026

---

## ⚡ Get Running in 5 Minutes

### Option 1: Run Without Docker (Local Development)

**Prerequisites:** Python 3.10+

```powershell
# Backend setup
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```powershell
# Frontend setup
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Then open in your browser:

- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

---

### Option 2: Run With Docker Compose

**Prerequisites:** Docker Desktop installed

```powershell
docker-compose build
docker-compose up -d
```

Then open:

- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

To stop:

```powershell
docker-compose down
```

---

## 🎯 Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:8501 | Streamlit user interface |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger UI documentation |
| Health Check | http://localhost:8000/health | Backend service health |
| Database | `backend/feedvote.db` | SQLite file for local development |

---

## ✨ Core Features to Try

1. Register a user from the sidebar
2. Submit an idea or feedback entry
3. Browse feedback and submit upvotes or downvotes
4. View the top ideas leaderboard

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 or 8501 in use | Stop the conflicting process or change ports |
| Python not found | Install Python 3.10+ from python.org |
| Backend not reachable | Confirm backend is running and `BACKEND_URL` is correct |
| Streamlit does not start | Verify frontend dependencies with `pip install -r requirements.txt` |
| Docker command not found | Install Docker Desktop and restart the terminal |

---

## 📚 More Documentation

- `README.md` — Overview and architecture
- `DOCKER_SETUP.md` — Docker development instructions
- `PROJECT_STATUS.md` — Current status and verification
- `DOCUMENTATION_INDEX.md` — Documentation guide

---

## Notes

- The frontend reads `BACKEND_URL` from environment variables; default is `http://localhost:8000`
- Production or Docker Hub deployment is not included in this repository
- Use `docker-compose` for local containerized development
